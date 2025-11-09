"""
Reminder tool for TaskFlow.
Handles setting, listing, and managing reminders with datetime parsing.
"""
import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pytz

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    HarmCategory = None
    HarmBlockThreshold = None

try:
    import dateparser
    DATEPARSER_AVAILABLE = True
except ImportError:
    DATEPARSER_AVAILABLE = False
    dateparser = None

from ..config import settings
from ..memory import MemoryStore

logger = logging.getLogger("taskflow")

# IST timezone
IST = pytz.timezone('Asia/Kolkata')


class ReminderTool:
    """Tool for setting and managing reminders."""
    
    def __init__(self, memory_store: Optional[MemoryStore] = None):
        """
        Initialize the reminder tool.
        
        Args:
            memory_store: MemoryStore instance for persisting reminders
        """
        self.memory_store = memory_store or MemoryStore()
        self.gemini_model = None
        
        # Initialize Gemini for datetime parsing if available
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
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
                logger.debug("Gemini model initialized for reminders")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini for reminders: {e}")
                self.gemini_model = None
    
    async def set_reminder(
        self,
        user_number: str,
        message: str,
        datetime_str: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Set a reminder.
        
        Args:
            user_number: User's phone number
            message: Reminder message/task description
            datetime_str: When to remind (ISO format or natural language)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with reminder status or error message
        """
        logger.info(f"⏰ Reminder requested: {message} at {datetime_str}")
        
        try:
            # Parse datetime
            if not datetime_str:
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": "When should I remind you? Please specify a date and time.",
                    "tool": "reminder"
                }
            
            parsed_datetime = await self._parse_datetime(datetime_str)
            if not parsed_datetime:
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": "I couldn't understand that date/time. Try formats like 'tomorrow at 3pm', 'Dec 10 at 3pm', or 'in 2 hours'.",
                    "tool": "reminder"
                }
            
            # Ensure datetime is in IST and in the future
            now_ist = datetime.now(IST)
            if parsed_datetime <= now_ist:
                return {
                    "success": False,
                    "message": "That time is in the past. Please set a reminder for a future time.",
                    "tool": "reminder"
                }
            
            # Create reminder
            reminder_id = str(uuid.uuid4())
            reminder_data = {
                "id": reminder_id,
                "task": message,
                "datetime": parsed_datetime.isoformat(),
                "status": "pending",
                "created_at": datetime.now(IST).isoformat()
            }
            
            # Save to memory
            self.memory_store.add_reminder(user_number, reminder_data)
            
            # Format response
            datetime_display = parsed_datetime.strftime("%b %d, %Y at %I:%M %p")
            active_count = len(self.memory_store.get_reminders(user_number, status="pending"))
            
            response = (
                f"✅ Reminder set!\n"
                f"📅 {datetime_display}\n"
                f"📝 {message}\n\n"
                f"You have {active_count} active reminder(s)."
            )
            
            return {
                "success": True,
                "message": response,
                "reminder_id": reminder_id,
                "tool": "reminder"
            }
            
        except Exception as e:
            logger.error(f"Error setting reminder: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Sorry, I encountered an error: {str(e)}",
                "tool": "reminder"
            }
    
    async def get_reminders(self, user_number: str) -> Dict[str, Any]:
        """
        Get all reminders for a user.
        
        Args:
            user_number: User's phone number
            
        Returns:
            Dictionary with reminders
        """
        logger.info(f"Getting reminders for {user_number}")
        
        try:
            reminders = self.memory_store.get_reminders(user_number, status="pending")
            
            if not reminders:
                return {
                    "success": True,
                    "reminders": [],
                    "message": "You have no active reminders. Set one with 'Remind me to...'",
                    "tool": "reminder"
                }
            
            # Sort by datetime
            reminders.sort(key=lambda x: x.get("datetime", ""))
            
            # Format reminders for display
            formatted_reminders = []
            for i, reminder in enumerate(reminders, 1):
                try:
                    reminder_dt = datetime.fromisoformat(reminder.get("datetime", ""))
                    if reminder_dt.tzinfo is None:
                        reminder_dt = IST.localize(reminder_dt)
                    datetime_display = reminder_dt.strftime("%b %d, %Y at %I:%M %p")
                except:
                    datetime_display = reminder.get("datetime", "Unknown")
                
                formatted_reminders.append({
                    "id": reminder.get("id"),
                    "number": i,
                    "task": reminder.get("task", "Unknown"),
                    "datetime": datetime_display,
                    "datetime_iso": reminder.get("datetime")
                })
            
            # Build response message
            message = f"📋 You have {len(reminders)} active reminder(s):\n\n"
            for reminder in formatted_reminders:
                message += f"{reminder['number']}. 📝 {reminder['task']}\n"
                message += f"   📅 {reminder['datetime']}\n\n"
            
            return {
                "success": True,
                "reminders": formatted_reminders,
                "message": message.strip(),
                "tool": "reminder"
            }
            
        except Exception as e:
            logger.error(f"Error getting reminders: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error retrieving reminders: {str(e)}",
                "tool": "reminder"
            }
    
    async def cancel_reminder(
        self,
        user_number: str,
        reminder_id: Optional[str] = None,
        reminder_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Cancel a reminder.
        
        Args:
            user_number: User's phone number
            reminder_id: Reminder ID to cancel
            reminder_number: Reminder number (1-based) to cancel
            
        Returns:
            Dictionary with cancellation status
        """
        logger.info(f"Cancel reminder requested for {user_number}: {reminder_id or reminder_number}")
        
        try:
            reminders = self.memory_store.get_reminders(user_number, status="pending")
            
            if not reminders:
                return {
                    "success": False,
                    "message": "You have no active reminders to cancel.",
                    "tool": "reminder"
                }
            
            # Sort by datetime
            reminders.sort(key=lambda x: x.get("datetime", ""))
            
            # Find reminder to cancel
            reminder_to_cancel = None
            
            if reminder_id:
                reminder_to_cancel = next((r for r in reminders if r.get("id") == reminder_id), None)
            elif reminder_number:
                if 1 <= reminder_number <= len(reminders):
                    reminder_to_cancel = reminders[reminder_number - 1]
            
            if not reminder_to_cancel:
                return {
                    "success": False,
                    "message": "Couldn't find that reminder. Use 'show my reminders' to see your active reminders.",
                    "tool": "reminder"
                }
            
            # Cancel reminder
            cancelled = self.memory_store.cancel_reminder(user_number, reminder_to_cancel.get("id"))
            
            if cancelled:
                task = reminder_to_cancel.get("task", "Reminder")
                active_count = len(self.memory_store.get_reminders(user_number, status="pending"))
                
                return {
                    "success": True,
                    "message": f"✅ Cancelled reminder: {task}\n\nYou have {active_count} active reminder(s) remaining.",
                    "tool": "reminder"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to cancel reminder. Please try again.",
                    "tool": "reminder"
                }
                
        except Exception as e:
            logger.error(f"Error cancelling reminder: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "tool": "reminder"
            }
    
    async def _parse_datetime(self, datetime_str: str) -> Optional[datetime]:
        """
        Parse flexible datetime strings into datetime objects.
        Handles formats like "tomorrow at 3pm", "Dec 10 at 3pm", "in 2 hours", etc.
        
        Args:
            datetime_str: Datetime string (flexible format)
            
        Returns:
            Datetime object in IST timezone or None if parsing fails
        """
        datetime_str = datetime_str.strip()
        
        # Try dateparser first (if available)
        if DATEPARSER_AVAILABLE:
            try:
                parsed = dateparser.parse(
                    datetime_str,
                    settings={'TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True}
                )
                if parsed:
                    # Ensure it's in IST
                    if parsed.tzinfo is None:
                        parsed = IST.localize(parsed)
                    else:
                        parsed = parsed.astimezone(IST)
                    return parsed
            except Exception as e:
                logger.debug(f"Dateparser failed: {e}")
        
        # Try Gemini if available
        if self.gemini_model:
            try:
                parsed = await self._parse_datetime_with_gemini(datetime_str)
                if parsed:
                    return parsed
            except Exception as e:
                logger.debug(f"Gemini datetime parsing failed: {e}")
        
        # Fallback: try simple patterns
        return self._parse_datetime_fallback(datetime_str)
    
    async def _parse_datetime_with_gemini(self, datetime_str: str) -> Optional[datetime]:
        """
        Use Gemini to parse flexible datetime strings.
        
        Args:
            datetime_str: Flexible datetime string
            
        Returns:
            Datetime object in IST or None
        """
        if not self.gemini_model:
            return None
        
        now_ist = datetime.now(IST)
        prompt = f"""Parse this datetime string into ISO 8601 format (YYYY-MM-DDTHH:MM:SS) in IST timezone.
Current time in IST: {now_ist.strftime("%Y-%m-%d %H:%M:%S %Z")}

Datetime string: "{datetime_str}"

Examples:
- "tomorrow at 3pm" -> {((now_ist + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)).isoformat()}
- "in 2 hours" -> {(now_ist + timedelta(hours=2)).isoformat()}
- "Dec 10 at 3pm" -> {now_ist.replace(month=12, day=10, hour=15, minute=0, second=0, microsecond=0).isoformat() if now_ist.month <= 12 else (now_ist.replace(year=now_ist.year+1, month=12, day=10, hour=15, minute=0, second=0, microsecond=0)).isoformat()}

Respond with ONLY the ISO datetime string in IST timezone, nothing else. If you cannot parse it, respond with "null"."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result = response.text.strip()
            
            if result.lower() == "null" or not result:
                return None
            
            # Parse ISO format
            try:
                parsed = datetime.fromisoformat(result.replace('Z', '+00:00'))
                # Convert to IST
                if parsed.tzinfo is None:
                    parsed = IST.localize(parsed)
                else:
                    parsed = parsed.astimezone(IST)
                return parsed
            except ValueError:
                return None
                
        except Exception as e:
            logger.warning(f"Gemini datetime parsing error: {e}")
            return None
    
    def _parse_datetime_fallback(self, datetime_str: str) -> Optional[datetime]:
        """
        Fallback datetime parsing using simple patterns.
        
        Args:
            datetime_str: Datetime string
            
        Returns:
            Datetime object in IST or None
        """
        now_ist = datetime.now(IST)
        datetime_lower = datetime_str.lower()
        
        # Relative times
        if "tomorrow" in datetime_lower:
            base_date = now_ist + timedelta(days=1)
            # Extract time if mentioned
            hour, minute = self._extract_time(datetime_str, base_date)
            return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        elif "in" in datetime_lower and ("hour" in datetime_lower or "hr" in datetime_lower):
            # "in 2 hours"
            import re
            match = re.search(r'in\s+(\d+)\s*(?:hour|hr)', datetime_lower)
            if match:
                hours = int(match.group(1))
                return now_ist + timedelta(hours=hours)
        
        elif "in" in datetime_lower and ("minute" in datetime_lower or "min" in datetime_lower):
            # "in 30 minutes"
            import re
            match = re.search(r'in\s+(\d+)\s*(?:minute|min)', datetime_lower)
            if match:
                minutes = int(match.group(1))
                return now_ist + timedelta(minutes=minutes)
        
        # Try to parse common date formats
        try:
            # Try ISO format
            parsed = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            if parsed.tzinfo is None:
                parsed = IST.localize(parsed)
            else:
                parsed = parsed.astimezone(IST)
            return parsed
        except:
            pass
        
        return None
    
    def _extract_time(self, datetime_str: str, base_date: datetime) -> tuple:
        """
        Extract hour and minute from datetime string.
        
        Args:
            datetime_str: Datetime string
            base_date: Base date to use
            
        Returns:
            Tuple of (hour, minute)
        """
        import re
        
        # Try to extract time patterns
        # "3pm", "3:30pm", "15:00", etc.
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm)',
            r'(\d{1,2})\s*(am|pm)',
            r'(\d{1,2}):(\d{2})',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, datetime_str.lower())
            if match:
                if len(match.groups()) == 3:  # hour:minute am/pm
                    hour = int(match.group(1))
                    minute = int(match.group(2))
                    am_pm = match.group(3)
                    if am_pm == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm == 'am' and hour == 12:
                        hour = 0
                    return (hour, minute)
                elif len(match.groups()) == 2:  # hour am/pm or hour:minute
                    if match.group(2) in ['am', 'pm']:  # hour am/pm
                        hour = int(match.group(1))
                        am_pm = match.group(2)
                        if am_pm == 'pm' and hour != 12:
                            hour += 12
                        elif am_pm == 'am' and hour == 12:
                            hour = 0
                        return (hour, 0)
                    else:  # hour:minute
                        hour = int(match.group(1))
                        minute = int(match.group(2))
                        return (hour, minute)
        
        # Default to current time
        return (base_date.hour, base_date.minute)
