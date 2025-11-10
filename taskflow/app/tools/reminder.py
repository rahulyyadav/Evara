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
                        logger.debug(f"Gemini model initialized for reminders with {model_name}")
                        break
                    except Exception as model_error:
                        logger.debug(f"Failed to initialize with {model_name}: {model_error}")
                        continue
                
                if not self.gemini_model:
                    logger.warning(f"Failed to initialize Gemini for reminders with any model")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini for reminders: {e}")
                self.gemini_model = None
    
    async def set_reminder(
        self,
        user_number: str,
        message: str,
        datetime_str: Optional[str] = None,
        country: Optional[str] = None,
        location: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Set a reminder.
        
        Args:
            user_number: User's phone number
            message: Reminder message/task description
            datetime_str: When to remind (ISO format or natural language)
            country: User's country for timezone (e.g., "India", "USA", "UK")
            location: User's city/location for timezone (alternative to country)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with reminder status or error message
        """
        logger.info(f"⏰ Reminder requested: {message} at {datetime_str} (country: {country}, location: {location})")
        
        try:
            # Check if we need time
            if not datetime_str:
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": "When should I remind you? Please specify a date and time. Also, please let me know your country or location so I can set the reminder in your local timezone.",
                    "tool": "reminder"
                }
            
            # Try to detect timezone from datetime_str if not explicitly provided
            if not country and not location:
                # Check if datetime_str mentions timezone/location
                datetime_lower = datetime_str.lower()
                if any(word in datetime_lower for word in ['india', 'indian', 'ist']):
                    country = "India"
                    logger.info("Auto-detected timezone: India (IST)")
                elif any(word in datetime_lower for word in ['usa', 'america', 'est', 'pst', 'cst']):
                    country = "USA"
                    logger.info("Auto-detected timezone: USA")
                elif any(word in datetime_lower for word in ['uk', 'britain', 'london', 'gmt', 'bst']):
                    country = "UK"
                    logger.info("Auto-detected timezone: UK")
                else:
                    # Default to IST if not specified (since most users are likely in India)
                    country = "India"
                    logger.info("Defaulting to India timezone (IST) as no timezone specified")
            
            # Get timezone based on country/location
            user_timezone = self._get_timezone_from_country(country, location)
            
            parsed_datetime = await self._parse_datetime(datetime_str, timezone=user_timezone)
            if not parsed_datetime:
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": "I couldn't understand that date/time. Try formats like 'tomorrow at 3pm', 'Dec 10 at 3pm', or 'in 2 hours'.",
                    "tool": "reminder"
                }
            
            # Ensure datetime is in user's timezone and in the future
            now_user_tz = datetime.now(user_timezone)
            if parsed_datetime <= now_user_tz:
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
                "timezone": str(user_timezone),
                "country": country,
                "location": location,
                "status": "pending",
                "created_at": datetime.now(user_timezone).isoformat()
            }
            
            # Save to memory
            self.memory_store.add_reminder(user_number, reminder_data)
            
            # Format response
            datetime_display = parsed_datetime.strftime("%b %d, %Y at %I:%M %p")
            active_count = len(self.memory_store.get_reminders(user_number, status="pending"))
            
            timezone_display = country or location or "your timezone"
            response = (
                f"✅ Reminder set!\n"
                f"📅 {datetime_display} ({timezone_display})\n"
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
    
    def _get_timezone_from_country(self, country: Optional[str], location: Optional[str]) -> pytz.timezone:
        """
        Get timezone from country or location.
        
        Args:
            country: Country name (e.g., "India", "USA", "UK")
            location: City/location name
            
        Returns:
            pytz timezone object (defaults to IST if not found)
        """
        # Common country to timezone mappings
        country_timezones = {
            "india": "Asia/Kolkata",
            "nepal": "Asia/Kathmandu",
            "usa": "America/New_York",
            "united states": "America/New_York",
            "uk": "Europe/London",
            "united kingdom": "Europe/London",
            "canada": "America/Toronto",
            "australia": "Australia/Sydney",
            "germany": "Europe/Berlin",
            "france": "Europe/Paris",
            "japan": "Asia/Tokyo",
            "china": "Asia/Shanghai",
            "singapore": "Asia/Singapore",
            "uae": "Asia/Dubai",
            "united arab emirates": "Asia/Dubai",
            "saudi arabia": "Asia/Riyadh",
        }
        
        # Try country first
        if country:
            country_lower = country.lower().strip()
            if country_lower in country_timezones:
                return pytz.timezone(country_timezones[country_lower])
        
        # Try location/city (common cities)
        if location:
            location_lower = location.lower().strip()
            # Common city mappings
            city_timezones = {
                "mumbai": "Asia/Kolkata",
                "delhi": "Asia/Kolkata",
                "bangalore": "Asia/Kolkata",
                "chennai": "Asia/Kolkata",
                "kolkata": "Asia/Kolkata",
                "kathmandu": "Asia/Kathmandu",
                "new york": "America/New_York",
                "los angeles": "America/Los_Angeles",
                "london": "Europe/London",
                "toronto": "America/Toronto",
                "sydney": "Australia/Sydney",
                "tokyo": "Asia/Tokyo",
            }
            if location_lower in city_timezones:
                return pytz.timezone(city_timezones[location_lower])
        
        # Default to IST
        logger.warning(f"Could not determine timezone for country={country}, location={location}, defaulting to IST")
        return IST
    
    async def _parse_datetime(self, datetime_str: str, timezone: Optional[pytz.timezone] = None) -> Optional[datetime]:
        """
        Parse flexible datetime strings into datetime objects.
        Handles formats like "tomorrow at 3pm", "Dec 10 at 3pm", "in 2 hours", etc.
        
        Args:
            datetime_str: Datetime string (flexible format)
            timezone: Target timezone (defaults to IST)
            
        Returns:
            Datetime object in specified timezone or None if parsing fails
        """
        if timezone is None:
            timezone = IST
        
        datetime_str = datetime_str.strip()
        
        # Try dateparser first (if available)
        if DATEPARSER_AVAILABLE:
            try:
                parsed = dateparser.parse(
                    datetime_str,
                    settings={'TIMEZONE': str(timezone), 'RETURN_AS_TIMEZONE_AWARE': True}
                )
                if parsed:
                    # Ensure it's in the correct timezone
                    if parsed.tzinfo is None:
                        parsed = timezone.localize(parsed)
                    else:
                        parsed = parsed.astimezone(timezone)
                    return parsed
            except Exception as e:
                logger.debug(f"Dateparser failed: {e}")
        
        # Try Gemini if available
        if self.gemini_model:
            try:
                parsed = await self._parse_datetime_with_gemini(datetime_str, timezone)
                if parsed:
                    return parsed
            except Exception as e:
                logger.debug(f"Gemini datetime parsing failed: {e}")
        
        # Fallback: try simple patterns
        return self._parse_datetime_fallback(datetime_str, timezone)
    
    async def _parse_datetime_with_gemini(self, datetime_str: str, timezone: Optional[pytz.timezone] = None) -> Optional[datetime]:
        """
        Use Gemini to parse flexible datetime strings with accurate current time context.
        
        Args:
            datetime_str: Flexible datetime string
            timezone: Target timezone (defaults to IST)
            
        Returns:
            Datetime object in specified timezone or None
        """
        if not self.gemini_model:
            return None
        
        if timezone is None:
            timezone = IST
        
        now_tz = datetime.now(timezone)
        now_utc = datetime.now(pytz.UTC)
        
        # Build comprehensive datetime context (like we did for date/time tracking)
        current_datetime_info = f"""Current Date and Time Information (CRITICAL - Use this for datetime parsing):

BASE TIME ({timezone}):
- Current datetime: {now_tz.strftime('%B %d, %Y at %I:%M:%S %p %Z')}
- Current date: {now_tz.strftime('%Y-%m-%d')}
- Current time: {now_tz.strftime('%H:%M:%S')} (24-hour) / {now_tz.strftime('%I:%M:%S %p')} (12-hour)
- Current day of week: {now_tz.strftime('%A')}
- ISO format: {now_tz.isoformat()}
- UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}
- Timezone: {timezone} ({now_tz.strftime('%Z')})

IMPORTANT DATETIME PARSING RULES:
1. ALWAYS use the current datetime shown above as reference
2. For "today at X PM", use {now_tz.strftime('%Y-%m-%d')} with the specified time
3. For "tomorrow at X PM", use {(now_tz + timedelta(days=1)).strftime('%Y-%m-%d')} with the specified time
4. For "in X hours/minutes", add to {now_tz.strftime('%H:%M:%S')}
5. For relative times, calculate from {now_tz.strftime('%I:%M %p %Z')}
6. Always use 24-hour format internally (convert PM times: 2 PM = 14:00, 3 PM = 15:00)
7. Be precise with seconds - default to :00 seconds if not specified
8. Be EXACT with time - "at 2PM" means exactly 14:00:00, not approximate

Examples based on current time being {now_tz.strftime('%B %d at %I:%M %p')}:
- "today at 2 PM" = {now_tz.strftime('%Y-%m-%d')}T14:00:00
- "tomorrow at 3 PM" = {(now_tz + timedelta(days=1)).strftime('%Y-%m-%d')}T15:00:00
- "in 2 hours" = {(now_tz + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')}
- "at 6:30 PM today" = {now_tz.strftime('%Y-%m-%d')}T18:30:00
"""
        
        prompt = f"""{current_datetime_info}

Datetime string to parse: "{datetime_str}"

Parse this into ISO 8601 format (YYYY-MM-DDTHH:MM:SS) using the current datetime information provided above.

CRITICAL: 
- Use the exact current time ({now_tz.strftime('%Y-%m-%d %H:%M:%S')}) shown above for all calculations
- Be precise with hours (convert PM correctly: 2 PM = 14:00, 3 PM = 15:00, 6 PM = 18:00)
- Default seconds to :00 if not specified
- Use {timezone} timezone
- Be EXACT - this is for reminders that need to fire at precise times

Respond with ONLY the ISO datetime string (YYYY-MM-DDTHH:MM:SS), nothing else. If you cannot parse it, respond with "null"."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result = response.text.strip()
            
            if result.lower() == "null" or not result:
                return None
            
            # Parse ISO format
            try:
                parsed = datetime.fromisoformat(result.replace('Z', '+00:00'))
                # Convert to target timezone
                if parsed.tzinfo is None:
                    parsed = timezone.localize(parsed)
                else:
                    parsed = parsed.astimezone(timezone)
                return parsed
            except ValueError:
                return None
                
        except Exception as e:
            logger.warning(f"Gemini datetime parsing error: {e}")
            return None
    
    def _parse_datetime_fallback(self, datetime_str: str, timezone: Optional[pytz.timezone] = None) -> Optional[datetime]:
        """
        Fallback datetime parsing using simple patterns.
        
        Args:
            datetime_str: Datetime string
            timezone: Target timezone (defaults to IST)
            
        Returns:
            Datetime object in specified timezone or None
        """
        if timezone is None:
            timezone = IST
        
        now_tz = datetime.now(timezone)
        datetime_lower = datetime_str.lower()
        
        # Relative times
        if "tomorrow" in datetime_lower:
            base_date = now_tz + timedelta(days=1)
            # Extract time if mentioned
            hour, minute = self._extract_time(datetime_str, base_date)
            return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        elif "in" in datetime_lower and ("hour" in datetime_lower or "hr" in datetime_lower):
            # "in 2 hours"
            import re
            match = re.search(r'in\s+(\d+)\s*(?:hour|hr)', datetime_lower)
            if match:
                hours = int(match.group(1))
                return now_tz + timedelta(hours=hours)
        
        elif "in" in datetime_lower and ("minute" in datetime_lower or "min" in datetime_lower):
            # "in 30 minutes"
            import re
            match = re.search(r'in\s+(\d+)\s*(?:minute|min)', datetime_lower)
            if match:
                minutes = int(match.group(1))
                return now_tz + timedelta(minutes=minutes)
        
        # Try to parse common date formats
        try:
            # Try ISO format
            parsed = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            if parsed.tzinfo is None:
                parsed = timezone.localize(parsed)
            else:
                parsed = parsed.astimezone(timezone)
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
