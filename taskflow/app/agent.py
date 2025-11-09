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
                # Try available models in order of preference
                model_names = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-flash-latest", "gemini-pro-latest"]
                self.gemini_model = None
                
                for model_name in model_names:
                    try:
                        self.gemini_model = genai.GenerativeModel(
                            model_name=model_name,
                            safety_settings={
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            }
                        )
                        logger.info(f"✅ Gemini model initialized successfully with {model_name}")
                        break
                    except Exception as model_error:
                        logger.debug(f"Failed to initialize with {model_name}: {model_error}")
                        continue
                
                if not self.gemini_model:
                    raise Exception(f"Failed to initialize with any model: {model_names}")
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
            prompt = f"""You are an AI assistant that classifies user messages into intents and extracts entities intelligently.

Available intents:
1. "flight_search" - User wants to search for flights (ANY phrasing: "flights from X to Y", "I need tickets X Y", "book flight X-Y", "can you find me flights to Y", "show flights between X and Y", "I want to travel X to Y", etc.)
2. "price_track" - User wants to track product prices, check tracked items, or stop tracking
3. "reminder" - User wants to set, list, or cancel reminders
4. "status_check" - User wants to check status of previous tasks
5. "general" - Casual conversation, greetings, general knowledge questions, or any question that doesn't fit the above categories

{context}

User message: "{message}"

Analyze the message and respond with ONLY a valid JSON object in this exact format:
{{
    "intent": "one_of_the_intents_above",
    "confidence": 0.0-1.0,
    "entities": {{
        "origin": "origin city/airport name - extract intelligently from ANY phrasing (e.g., 'from X', 'X to Y', 'X-Y', 'X Y', 'leaving X', 'departing X', 'starting from X', or first city mentioned)",
        "destination": "destination city/airport name - extract intelligently from ANY phrasing (e.g., 'to Y', 'X to Y', 'X-Y', 'X Y', 'going to Y', 'arriving at Y', 'destination Y', or second city mentioned)",
        "date": "date in original format as mentioned by user (e.g., 'next Tuesday', 'Dec 15', 'next Friday', 'tomorrow', '3rd December', '15/12', etc.)",
        "product": "product name if price tracking (extract from any phrasing like 'track iPhone', 'iPhone price', 'search iPhone')",
        "url": "product URL if price tracking (extract from any phrasing containing URL or link)",
        "price_action": "action for price tracking: 'track' (default), 'check' (show tracked items), or 'stop' (stop tracking)",
        "target_price": "target price if mentioned (extract numbers like 'below 50000', 'under ₹50000', 'when it's 50000')",
        "reminder_text": "reminder message if reminder",
        "reminder_time": "time/date for reminder if mentioned",
        "reminder_country": "user's country or location (e.g., 'India', 'USA', 'UK', 'Canada', 'Australia') for timezone",
        "reminder_location": "user's city or location for timezone (alternative to country)",
        "reminder_action": "action for reminder: 'set', 'list', or 'cancel'",
        "reminder_number": "reminder number if cancelling by number",
        "reminder_id": "reminder ID if cancelling by ID",
        "message": "original message for context"
    }},
    "needs_clarification": true/false,
    "clarification_question": "question to ask if needs_clarification is true"
}}

CRITICAL INSTRUCTIONS FOR FLIGHT SEARCH:
- Be VERY flexible in understanding flight queries - users may phrase them in ANY way
- Extract origin and destination from ANY format: "X to Y", "X-Y", "X Y", "from X to Y", "X going to Y", "flights between X and Y", "tickets X Y", etc.
- If user says "flights to Y" or "I want to go to Y", extract destination=Y, origin=null
- If user says "flights from X" or "leaving from X", extract origin=X, destination=null
- If two cities are mentioned, the first is usually origin, second is destination
- For dates: Extract ANY date format mentioned - be flexible with "next Tuesday", "Dec 3rd", "3rd Dec", "15/12", "2024-12-15", etc.
- Only set needs_clarification=true if BOTH origin AND destination are missing (or if it's truly unclear)
- If only one city is mentioned, try to infer if it's origin or destination from context

CRITICAL INSTRUCTIONS FOR PRICE TRACKING:
- Be VERY flexible in understanding price tracking queries - users may phrase them in ANY way
- Extract product name from ANY phrasing: "track iPhone", "iPhone price", "search iPhone", "find iPhone", "check iPhone price", "monitor iPhone", etc.
- Extract URL if user provides a link or says "track this" with a URL
- Extract target_price from phrases like "below 50000", "under ₹50000", "when it's 50000", "alert me at 50000", etc.
- price_action should be: "track" (default for new tracking), "check" (show tracked items), or "stop" (stop tracking)
- Examples:
  - "track iPhone 15" → product="iPhone 15", price_action="track"
  - "search me price of iphone 17" → product="iphone 17", price_action="track"
  - "check my tracked items" → price_action="check"
  - "stop tracking iPhone" → product="iPhone", price_action="stop"
  - "track iPhone below 50000" → product="iPhone", target_price=50000, price_action="track"

Examples of flexible extraction:
- "can you track flight from chennai to bagdogra on dec 3rd" → origin="chennai", destination="bagdogra", date="dec 3rd"
- "find flights to mumbai next tuesday" → origin=null, destination="mumbai", date="next tuesday"
- "I need tickets chennai bagdogra" → origin="chennai", destination="bagdogra", date=null
- "book me a flight from delhi going to goa tomorrow" → origin="delhi", destination="goa", date="tomorrow"
- "show me flights between mumbai and delhi" → origin="mumbai", destination="delhi" (or vice versa based on context)

Important:
- Return ONLY the JSON object, no other text
- Use null for missing entities
- Be confident and intelligent in entity extraction
- Handle ANY phrasing or twisted way of asking for flights
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
                # Clean and normalize entity values
                origin = entities.get("origin")
                destination = entities.get("destination")
                date = entities.get("date")
                
                # Remove None, empty strings, and "null" strings
                origin = origin if origin and origin.lower() != "null" else None
                destination = destination if destination and destination.lower() != "null" else None
                date = date if date and date.lower() != "null" else None
                
                logger.info(f"🔍 Flight search entities - Origin: {origin}, Destination: {destination}, Date: {date}")
                
                result = await self.flight_tool.search(
                    origin=origin,
                    destination=destination,
                    date=date
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
                    # Parse target_price if provided (could be string or number)
                    target_price = entities.get("target_price")
                    if target_price:
                        try:
                            # Try to convert to float if it's a string
                            if isinstance(target_price, str):
                                # Remove currency symbols and extract number
                                import re
                                price_match = re.search(r'(\d+\.?\d*)', target_price.replace(',', ''))
                                if price_match:
                                    target_price = float(price_match.group(1))
                                else:
                                    target_price = None
                            else:
                                target_price = float(target_price)
                        except (ValueError, TypeError):
                            target_price = None
                    
                    result = await self.price_tool.track_product(
                        user_number=user_number,
                        url=entities.get("url"),
                        product_name=entities.get("product"),
                        target_price=target_price
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
                    # Get user's stored timezone/country from preferences
                    user_memory = self.memory_store.get_user_memory(user_number)
                    user_country = user_memory.get("preferences", {}).get("country") or entities.get("reminder_country")
                    user_location = user_memory.get("preferences", {}).get("location") or entities.get("reminder_location")
                    
                    result = await self.reminder_tool.set_reminder(
                        user_number=user_number,
                        message=entities.get("reminder_text", ""),
                        datetime_str=entities.get("reminder_time"),
                        country=user_country,
                        location=user_location
                    )
                    
                    # If reminder was set successfully and we got country/location, save it to preferences
                    if result.get("success") and (user_country or user_location):
                        preferences = user_memory.get("preferences", {})
                        if user_country:
                            preferences["country"] = user_country
                        if user_location:
                            preferences["location"] = user_location
                        self.memory_store.update_preferences(user_number, preferences)
                    
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
            # For general questions, we MUST have Gemini - return error message
            if intent == self.INTENT_GENERAL:
                logger.error("Gemini model not available but required for general questions")
                return "I'm sorry, but I need my AI capabilities to answer general questions. Please ensure GEMINI_API_KEY is configured."
            # Fallback response generation for other intents
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
            
            # For general questions, use a more direct prompt
            if intent == self.INTENT_GENERAL:
                # Information about Evara (only use when explicitly asked)
                evara_info = """
About Evara - IMPORTANT: Only share this information if the user EXPLICITLY asks about it:

Your Identity:
- You are Evara, an AI agent created by Rahul Yadav
- When asked "which model are you using" or "what model are you" or "what are you":
  → Reply clearly and formally: "I am Evara, an AI agent created by Rahul Yadav."

Creator Information:
- Created by: Rahul Yadav
- When asked "who made you" or "who created you" or "who is your creator" or "who made this agent":
  → Reply clearly: "I was created by Rahul Yadav."

Contact Information:
- Email: rahulyyadav21@gmail.com
- When asked for "contact" or "email" or "how to contact" or "your email":
  → Reply: "rahulyyadav21@gmail.com"

CRITICAL: Do NOT mention any of this information (name, creator, contact) unless the user specifically asks about it. Keep responses focused only on what the user asked.
"""
                
                prompt = f"""You are Evara, a helpful and knowledgeable AI assistant on WhatsApp.

{evara_info}

{context}

User asked: "{message}"

Please provide a helpful, accurate, and concise answer to the user's question. 
- Answer general knowledge questions directly and accurately
- Be conversational and friendly
- Use emojis sparingly (1-2 max)
- Keep response under 1600 characters
- Format for WhatsApp (short paragraphs, easy to read)
- If you don't know something, say so honestly
- Only mention information about Evara's creator/contact if the user explicitly asks

Respond directly with your answer, no JSON or code blocks. Just the answer text."""
            else:
                # Information about Evara (only use when explicitly asked)
                evara_info = """
About Evara - IMPORTANT: Only share this information if the user EXPLICITLY asks about it:

Your Identity:
- You are Evara, an AI agent created by Rahul Yadav
- When asked "which model are you using" or "what model are you" or "what are you":
  → Reply clearly and formally: "I am Evara, an AI agent created by Rahul Yadav."

Creator Information:
- Created by: Rahul Yadav
- When asked "who made you" or "who created you" or "who is your creator" or "who made this agent":
  → Reply clearly: "I was created by Rahul Yadav."

Contact Information:
- Email: rahulyyadav21@gmail.com
- When asked for "contact" or "email" or "how to contact" or "your email":
  → Reply: "rahulyyadav21@gmail.com"

CRITICAL: Do NOT mention any of this information (name, creator, contact) unless the user specifically asks about it. Keep responses focused only on what the user asked.
"""
                
                prompt = f"""You are Evara, a helpful WhatsApp AI assistant that helps users with:
- Flight searches
- Price tracking
- Reminders
- General questions

{evara_info}

{context}

User message: "{message}"
Detected intent: {intent}
Extracted entities: {json.dumps(entities, indent=2)}
{tool_info}

Generate a friendly, concise response (under 1600 characters) that:
1. Is natural and conversational
2. Addresses the user's request
3. If tool was executed, explains the result clearly
4. If clarification is needed, asks a helpful question in a friendly way (e.g., "I'd be happy to help! Could you tell me [missing info]?")
5. Uses emojis appropriately (but not excessively)
6. Is formatted for WhatsApp (short paragraphs, bullet points if needed)
7. Only mention information about Evara's creator/contact if the user explicitly asks
8. For flight search: If clarification is needed, be helpful and ask for missing info (origin, destination, or date) in a friendly, conversational way

Respond directly with the message text, no JSON or code blocks."""
            
            response = await self._call_gemini_with_retry(prompt, max_retries=3)
            
            # Clean up response
            response = response.strip()
            
            # Remove quotes if wrapped
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            
            # Remove markdown code blocks if present
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1]) if len(lines) > 2 else response
                response = response.strip()
            
            # For general questions, ensure we got a real response
            if intent == self.INTENT_GENERAL and (not response or len(response) < 10):
                logger.warning(f"Gemini returned very short response for general question: {response}")
                # Try once more with a simpler prompt
                simple_prompt = f"User asked: {message}\n\nPlease provide a helpful answer:"
                try:
                    response = await self._call_gemini_with_retry(simple_prompt, max_retries=2)
                    response = response.strip()
                except Exception as retry_error:
                    logger.error(f"Retry also failed: {retry_error}")
                    return "I apologize, but I'm having trouble processing your question right now. Please try again."
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            # For general questions, don't fall back to default message
            if intent == self.INTENT_GENERAL:
                return f"I apologize, but I encountered an error while processing your question. Please try rephrasing it."
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
            self.INTENT_GENERAL: "Hello! I'm Evara, your AI assistant. I can help with flights, price tracking, and reminders. What would you like to do?"
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
        message = f"✈️ *Flight Search Results*\n\n"
        message += f"📍 {origin} → {destination}\n"
        message += f"📅 {date}\n\n"
        message += f"Found {len(flights)} flight(s):\n\n"
        
        for i, flight in enumerate(flights, 1):
            airline = flight.get("airline", "Unknown")
            price = flight.get("price", "N/A")
            dep_time = flight.get("departure_time", "N/A")
            arr_time = flight.get("arrival_time", "N/A")
            stops = flight.get("stops", "Direct")
            booking_link = flight.get("booking_link")
            
            message += f"*{i}. {airline}*\n"
            message += f"💰 {price}\n"
            message += f"⏰ {dep_time} → {arr_time}\n"
            message += f"🛫 {stops}\n"
            
            if booking_link:
                message += f"🔗 Book: {booking_link}\n"
            
            if i < len(flights):
                message += "\n"
        
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

