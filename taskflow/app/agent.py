"""
Agent orchestration logic for TaskFlow.
Uses Google Gemini API to understand user intent and coordinate tool execution.
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    HarmCategory = None
    HarmBlockThreshold = None

from .config import settings
from .memory import MemoryStore
from .tools import FlightSearchTool, PriceTrackerTool, ReminderTool

logger = logging.getLogger("taskflow")


class AgentOrchestrator:
    """
    Main agent orchestrator that processes messages, classifies intent,
    executes tools, and generates responses.
    """
    
    # Intent categories
    INTENT_FLIGHT_SEARCH = "flight_search"
    INTENT_PRICE_TRACK = "price_track"
    INTENT_REMINDER = "reminder"
    INTENT_STATUS_CHECK = "status_check"
    INTENT_GENERAL = "general"
    
    # Maximum response length for WhatsApp (1600 chars)
    MAX_RESPONSE_LENGTH = 1600
    
    def __init__(self):
        """Initialize the agent orchestrator."""
        self.memory_store = MemoryStore()
        self.flight_tool = FlightSearchTool()
        self.price_tool = PriceTrackerTool(memory_store=self.memory_store)
        self.reminder_tool = ReminderTool(memory_store=self.memory_store)
        
        # Initialize Gemini
        if not GEMINI_AVAILABLE:
            logger.warning("google-generativeai package not installed - agent will have limited functionality")
            self.gemini_model = None
        elif not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set - agent will have limited functionality")
            self.gemini_model = None
        else:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }
                )
                logger.info("✅ Gemini model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_model = None
    
    async def process_message(
        self,
        user_number: str,
        message: str
    ) -> str:
        """
        Process incoming message and generate response.
        
        Args:
            user_number: User's phone number
            message: User's message content
            
        Returns:
            Response message to send to user
        """
        logger.info(f"🤖 Processing message from {user_number}: {message[:100]}...")
        
        try:
            # Load user memory for context
            user_memory = self.memory_store.get_user_memory(user_number)
            recent_conversations = self.memory_store.get_recent_conversations(user_number, limit=5)
            
            # Classify intent and extract entities
            intent_result = await self._classify_intent(message, recent_conversations)
            intent = intent_result.get("intent", self.INTENT_GENERAL)
            entities = intent_result.get("entities", {})
            confidence = intent_result.get("confidence", 0.0)
            
            logger.info(f"📊 Intent: {intent} (confidence: {confidence:.2f})")
            logger.debug(f"📋 Entities: {entities}")
            
            # Store message for action detection
            self._last_message = message
            
            # Execute tool if needed
            tool_result = None
            if intent != self.INTENT_GENERAL and intent != self.INTENT_STATUS_CHECK:
                tool_result = await self._execute_tool(intent, entities, user_number, message)
            
            # Handle status check
            if intent == self.INTENT_STATUS_CHECK:
                tool_result = await self._check_status(user_number)
            
            # Generate natural language response
            response = await self._generate_response(
                message=message,
                intent=intent,
                entities=entities,
                tool_result=tool_result,
                recent_conversations=recent_conversations
            )
            
            # Truncate if too long
            if len(response) > self.MAX_RESPONSE_LENGTH:
                response = response[:self.MAX_RESPONSE_LENGTH - 3] + "..."
                logger.warning(f"Response truncated to {self.MAX_RESPONSE_LENGTH} chars")
            
            # Save conversation to memory
            tool_used = tool_result.get("tool") if tool_result else None
            self.memory_store.add_conversation(user_number, message, response, intent, tool_used)
            
            logger.info(f"✅ Generated response: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}", exc_info=True)
            from .utils.messages import get_friendly_error_message
            return get_friendly_error_message("processing")
    
    async def _classify_intent(
        self,
        message: str,
        recent_conversations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Classify user intent using Gemini.
        
        Args:
            message: User's message
            recent_conversations: Recent conversation history for context
            
        Returns:
            Dictionary with intent, entities, and confidence
        """
        if not self.gemini_model:
            # Fallback to simple keyword matching if Gemini not available
            return self._fallback_intent_classification(message)
        
        try:
            # Build context from recent conversations
            context = ""
            if recent_conversations:
                context = "Recent conversation history:\n"
                for conv in recent_conversations[-3:]:  # Last 3 conversations
                    context += f"User: {conv.get('message', '')}\n"
                    context += f"Assistant: {conv.get('response', '')}\n\n"
            
            # Create structured prompt for intent classification
            prompt = f"""You are an AI assistant that classifies user messages into intents.

Available intents:
1. "flight_search" - User wants to search for flights (e.g., "flights from Delhi to Mumbai", "cheap flights to Goa")
2. "price_track" - User wants to track product prices, check tracked items, or stop tracking (e.g., "track iPhone price", "check tracked items", "stop tracking iPhone")
3. "reminder" - User wants to set, list, or cancel reminders (e.g., "remind me to call mom", "show my reminders", "cancel reminder 1")
4. "status_check" - User wants to check status of previous tasks (e.g., "check my flights", "what am I tracking", "show my reminders")
5. "general" - Casual conversation, greetings, questions (e.g., "hello", "how are you", "what can you do")

{context}

User message: "{message}"

Analyze the message and respond with ONLY a valid JSON object in this exact format:
{{
    "intent": "one_of_the_intents_above",
    "confidence": 0.0-1.0,
    "entities": {{
        "origin": "city/airport if flight search",
        "destination": "city/airport if flight search",
        "date": "date if mentioned",
        "product": "product name if price tracking",
        "url": "product URL if price tracking",
        "price_action": "action for price tracking: 'track', 'check', or 'stop' (e.g., 'stop tracking iPhone' -> price_action='stop')",
        "target_price": "target price if mentioned",
        "reminder_text": "reminder message if reminder",
        "reminder_time": "time/date for reminder if mentioned",
        "reminder_action": "action for reminder: 'set', 'list', or 'cancel' (e.g., 'cancel reminder 1' -> reminder_action='cancel')",
        "reminder_number": "reminder number if cancelling by number",
        "reminder_id": "reminder ID if cancelling by ID",
        "message": "original message for context"
    }},
    "needs_clarification": true/false,
    "clarification_question": "question to ask if needs_clarification is true"
}}

Important:
- Return ONLY the JSON object, no other text
- Use null for missing entities
- Be confident in intent classification
- If unclear, set needs_clarification to true and provide a helpful question
"""
            
            # Call Gemini with retry logic
            response = await self._call_gemini_with_retry(prompt, max_retries=3)
            
            # Parse JSON response
            try:
                # Extract JSON from response (handle markdown code blocks)
                response_text = response.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                result = json.loads(response_text)
                
                # Validate intent
                valid_intents = [
                    self.INTENT_FLIGHT_SEARCH,
                    self.INTENT_PRICE_TRACK,
                    self.INTENT_REMINDER,
                    self.INTENT_STATUS_CHECK,
                    self.INTENT_GENERAL
                ]
                if result.get("intent") not in valid_intents:
                    logger.warning(f"Invalid intent returned: {result.get('intent')}, defaulting to general")
                    result["intent"] = self.INTENT_GENERAL
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Gemini JSON response: {e}")
                logger.debug(f"Response was: {response}")
                return self._fallback_intent_classification(message)
                
        except Exception as e:
            logger.error(f"Error in intent classification: {e}")
            return self._fallback_intent_classification(message)
    
    def _fallback_intent_classification(self, message: str) -> Dict[str, Any]:
        """
        Fallback intent classification using keyword matching.
        Used when Gemini is not available.
        
        Args:
            message: User's message
            
        Returns:
            Dictionary with intent classification
        """
        message_lower = message.lower()
        
        # Keyword-based classification
        if any(word in message_lower for word in ["flight", "fly", "airline", "ticket", "book flight"]):
            intent = self.INTENT_FLIGHT_SEARCH
        elif any(word in message_lower for word in ["track", "price", "monitor", "alert", "cheap"]):
            intent = self.INTENT_PRICE_TRACK
        elif any(word in message_lower for word in ["remind", "reminder", "remember"]):
            intent = self.INTENT_REMINDER
        elif any(word in message_lower for word in ["status", "check", "show", "list", "what am i"]):
            intent = self.INTENT_STATUS_CHECK
        else:
            intent = self.INTENT_GENERAL
        
        return {
            "intent": intent,
            "confidence": 0.5,  # Lower confidence for fallback
            "entities": {},
            "needs_clarification": False
        }
    
    async def _execute_tool(
        self,
        intent: str,
        entities: Dict[str, Any],
        user_number: str,
        message: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Execute appropriate tool based on intent.
        
        Args:
            intent: Classified intent
            entities: Extracted entities
            user_number: User's phone number
            
        Returns:
            Tool execution result or None
        """
        logger.info(f"🔧 Executing tool for intent: {intent}")
        
        try:
            if intent == self.INTENT_FLIGHT_SEARCH:
                result = await self.flight_tool.search(
                    origin=entities.get("origin"),
                    destination=entities.get("destination"),
                    date=entities.get("date")
                )
                return result
            
            elif intent == self.INTENT_PRICE_TRACK:
                # Check if user wants to stop tracking or check tracked items
                message_lower = message.lower()
                action = entities.get("price_action", "").lower()
                
                # Detect action from message if not in entities
                if not action:
                    if "stop tracking" in message_lower or "remove tracking" in message_lower or "untrack" in message_lower:
                        action = "stop"
                    elif "check tracked" in message_lower or "show tracked" in message_lower or "list tracked" in message_lower:
                        action = "check"
                
                if action == "stop":
                    result = await self.price_tool.stop_tracking(
                        user_number=user_number,
                        product_id=entities.get("product_id"),
                        product_name=entities.get("product")
                    )
                elif action == "check":
                    result = await self.price_tool.get_tracked_items(user_number)
                else:
                    result = await self.price_tool.track_product(
                        user_number=user_number,
                        url=entities.get("url"),
                        product_name=entities.get("product"),
                        target_price=entities.get("target_price")
                    )
                return result
            
            elif intent == self.INTENT_REMINDER:
                # Check if user wants to cancel or list reminders
                message_lower = message.lower()
                action = entities.get("reminder_action", "").lower()
                
                # Detect action from message if not in entities
                if not action:
                    if "cancel reminder" in message_lower or "delete reminder" in message_lower or "remove reminder" in message_lower:
                        action = "cancel"
                    elif "show reminder" in message_lower or "list reminder" in message_lower or "my reminder" in message_lower:
                        action = "list"
                
                if action == "cancel":
                    # Try to extract reminder number or ID
                    reminder_number = entities.get("reminder_number")
                    reminder_id = entities.get("reminder_id")
                    result = await self.reminder_tool.cancel_reminder(
                        user_number=user_number,
                        reminder_id=reminder_id,
                        reminder_number=reminder_number
                    )
                elif action == "list":
                    result = await self.reminder_tool.get_reminders(user_number)
                else:
                    result = await self.reminder_tool.set_reminder(
                        user_number=user_number,
                        message=entities.get("reminder_text", ""),
                        datetime_str=entities.get("reminder_time")
                    )
                return result
            
            else:
                logger.warning(f"No tool available for intent: {intent}")
                return None
                
        except Exception as e:
            logger.error(f"Error executing tool: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "message": "An error occurred while executing the tool."
            }
    
    async def _check_status(self, user_number: str) -> Dict[str, Any]:
        """
        Check status of user's tracked items and reminders.
        
        Args:
            user_number: User's phone number
            
        Returns:
            Dictionary with status information
        """
        logger.info(f"📊 Checking status for {user_number}")
        
        try:
            # Get tracked items
            tracked_items = await self.price_tool.get_tracked_items(user_number)
            
            # Get reminders
            reminders = await self.reminder_tool.get_reminders(user_number)
            
            return {
                "success": True,
                "tracked_items": tracked_items.get("items", []),
                "reminders": reminders.get("reminders", []),
                "tool": "status_check"
            }
        except Exception as e:
            logger.error(f"Error checking status: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_response(
        self,
        message: str,
        intent: str,
        entities: Dict[str, Any],
        tool_result: Optional[Dict[str, Any]],
        recent_conversations: List[Dict[str, Any]]
    ) -> str:
        """
        Generate natural language response using Gemini.
        
        Args:
            message: Original user message
            intent: Classified intent
            entities: Extracted entities
            tool_result: Result from tool execution (if any)
            recent_conversations: Recent conversation history
            
        Returns:
            Natural language response
        """
        if not self.gemini_model:
            # Fallback response generation
            return self._fallback_response_generation(intent, tool_result)
        
        try:
            # Build context
            context = ""
            if recent_conversations:
                context = "Recent conversation:\n"
                for conv in recent_conversations[-2:]:
                    context += f"User: {conv.get('message', '')}\n"
                    context += f"Assistant: {conv.get('response', '')}\n\n"
            
            # Build prompt
            tool_info = ""
            if tool_result:
                tool_info = f"\nTool execution result:\n{json.dumps(tool_result, indent=2)}"
            
            prompt = f"""You are TaskFlow, a helpful WhatsApp AI assistant that helps users with:
- Flight searches
- Price tracking
- Reminders
- General questions

{context}

User message: "{message}"
Detected intent: {intent}
Extracted entities: {json.dumps(entities, indent=2)}
{tool_info}

Generate a friendly, concise response (under 1600 characters) that:
1. Is natural and conversational
2. Addresses the user's request
3. If tool was executed, explains the result clearly
4. If clarification is needed, asks a helpful question
5. Uses emojis appropriately (but not excessively)
6. Is formatted for WhatsApp (short paragraphs, bullet points if needed)

Respond directly with the message text, no JSON or code blocks."""
            
            response = await self._call_gemini_with_retry(prompt, max_retries=3)
            
            # Clean up response
            response = response.strip()
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response_generation(intent, tool_result)
    
    def _fallback_response_generation(
        self,
        intent: str,
        tool_result: Optional[Dict[str, Any]]
    ) -> str:
        """
        Fallback response generation when Gemini is not available.
        
        Args:
            intent: Classified intent
            tool_result: Tool execution result
            
        Returns:
            Fallback response message
        """
        if tool_result:
            # Handle flight search results
            if intent == self.INTENT_FLIGHT_SEARCH and tool_result.get("tool") == "flight_search":
                if tool_result.get("success") and tool_result.get("flights"):
                    return self._format_flight_results(tool_result)
                elif tool_result.get("needs_clarification"):
                    return tool_result.get("message", "I need more information to search flights.")
                else:
                    return tool_result.get("message", "I encountered an issue searching for flights.")
            
            # Handle price tracker results
            if intent == self.INTENT_PRICE_TRACK and tool_result.get("tool") == "price_tracker":
                if tool_result.get("needs_clarification"):
                    return tool_result.get("message", "I need more information to track prices.")
                else:
                    return tool_result.get("message", tool_result.get("message", "Price tracking completed."))
            
            # Handle reminder results
            if intent == self.INTENT_REMINDER and tool_result.get("tool") == "reminder":
                if tool_result.get("needs_clarification"):
                    return tool_result.get("message", "I need more information to set a reminder.")
                else:
                    return tool_result.get("message", tool_result.get("message", "Reminder completed."))
            
            # Handle other tool results
            if tool_result.get("success"):
                return tool_result.get("message", "Task completed successfully!")
            else:
                return tool_result.get("message", "I encountered an issue, but I'm working on it!")
        
        # Intent-based responses
        responses = {
            self.INTENT_FLIGHT_SEARCH: "I can help you search for flights! Please provide origin, destination, and date.",
            self.INTENT_PRICE_TRACK: "I can help you track product prices! Send me a product name or URL.",
            self.INTENT_REMINDER: "I can set reminders for you! What would you like to be reminded about?",
            self.INTENT_STATUS_CHECK: "Let me check your tracked items and reminders...",
            self.INTENT_GENERAL: "Hello! I'm TaskFlow, your AI assistant. I can help with flights, price tracking, and reminders. What would you like to do?"
        }
        
        return responses.get(intent, "How can I help you today?")
    
    def _format_flight_results(self, tool_result: Dict[str, Any]) -> str:
        """
        Format flight search results for WhatsApp display.
        
        Args:
            tool_result: Flight search result dictionary
            
        Returns:
            Formatted message string
        """
        flights = tool_result.get("flights", [])
        origin = tool_result.get("origin", "Unknown")
        destination = tool_result.get("destination", "Unknown")
        date = tool_result.get("date", "Unknown")
        
        if not flights:
            return f"✈️ No flights found from {origin} to {destination} on {date}. Try different dates?"
        
        # Build response message
        message = f"✈️ Found {len(flights)} flight(s) from {origin} to {destination} on {date}:\n\n"
        
        for i, flight in enumerate(flights, 1):
            airline = flight.get("airline", "Unknown")
            price = flight.get("price", "N/A")
            dep_time = flight.get("departure_time", "N/A")
            arr_time = flight.get("arrival_time", "N/A")
            stops = flight.get("stops", "Direct")
            booking_link = flight.get("booking_link")
            
            message += f"✈️ {airline} - {price}\n"
            message += f"⏰ {dep_time} - {arr_time} ({stops})\n"
            
            if booking_link:
                message += f"🔗 {booking_link}\n"
            
            if i < len(flights):
                message += "\n"
        
        message += "\nWant me to check baggage options or flexible dates?"
        
        return message
    
    async def _call_gemini_with_retry(
        self,
        prompt: str,
        max_retries: int = 3
    ) -> str:
        """
        Call Gemini API with retry logic.
        
        Args:
            prompt: Prompt to send
            max_retries: Maximum number of retry attempts
            
        Returns:
            Gemini response text
            
        Raises:
            Exception: If all retries fail
        """
        if not self.gemini_model:
            raise Exception("Gemini model not initialized")
        
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.debug(f"Calling Gemini (attempt {attempt + 1}/{max_retries})")
                response = self.gemini_model.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("Empty response from Gemini API")
                
                return response.text
            except Exception as e:
                last_error = e
                logger.warning(f"Gemini API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # Wait before retry (exponential backoff)
                    await asyncio.sleep(2 ** attempt)
        
        raise Exception(f"Gemini API call failed after {max_retries} attempts: {last_error}")

