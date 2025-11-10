"""
Flight search tool for TaskFlow.
Uses SerpAPI to search for flights and return results.
Enhanced with accurate date tracking and parsing.
"""
import asyncio
import json
import logging
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

import httpx

from ..config import settings

logger = logging.getLogger("taskflow")

# IST timezone for accurate date tracking
IST = pytz.timezone('Asia/Kolkata')


class FlightSearchTool:
    """Tool for searching flights using SerpAPI Google Flights API."""
    
    # Cache duration: 1 hour
    CACHE_DURATION = timedelta(hours=1)
    
    
    def __init__(self):
        """Initialize the flight search tool."""
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.gemini_model = None
        
        # Initialize Gemini for date parsing if available
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
                        logger.debug(f"Gemini model initialized for flight search with {model_name}")
                        break
                    except Exception as model_error:
                        logger.debug(f"Failed to initialize with {model_name}: {model_error}")
                        continue
                
                if not self.gemini_model:
                    logger.warning(f"Failed to initialize Gemini for flight search with any model")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini for flight search: {e}")
                self.gemini_model = None
        else:
            self.gemini_model = None
    
    async def search(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        date: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for flights.
        
        Args:
            origin: Origin city/airport
            destination: Destination city/airport
            date: Travel date (can be flexible like "next Friday", "Dec 15", "2024-12-15")
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with search results or error message
        """
        logger.info(f"✈️ Flight search: {origin} -> {destination} on {date}")
        
        # Check if we need clarification
        # Destination is required, origin can be optional (user might just say "flights to Mumbai")
        if not destination:
            return {
                "success": False,
                "needs_clarification": True,
                "message": "I need the destination city to search flights. Where would you like to go?",
                "tool": "flight_search"
            }
        
        # If origin is missing, we can still search but might need to ask
        if not origin:
            # Try to infer from context or ask user
            return {
                "success": False,
                "needs_clarification": True,
                "message": "I need the origin city to search flights. Where are you flying from?",
                "tool": "flight_search"
            }
        
        # Parse and normalize date
        logger.info(f"📅 Parsing date: '{date}'")
        parsed_date = await self._parse_date(date)
        if not parsed_date:
            logger.warning(f"❌ Failed to parse date: '{date}'")
            return {
                "success": False,
                "needs_clarification": True,
                "message": "I couldn't understand the date. Please specify a date like 'Dec 15', 'next Friday', or '2024-12-15'.",
                "tool": "flight_search"
            }
        logger.info(f"✅ Parsed date: '{date}' → {parsed_date}")
        
        # Validate date is in the future (using IST timezone for accuracy)
        try:
            parsed_dt = datetime.strptime(parsed_date, "%Y-%m-%d")
            today_ist = datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            if parsed_dt < today_ist:
                # Format date nicely for user
                parsed_display = parsed_dt.strftime("%B %d, %Y")
                today_display = today_ist.strftime("%B %d, %Y")
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": f"That date ({parsed_display}) is in the past. Today is {today_display}. Please provide a future date for your flight search.",
                    "tool": "flight_search"
                }
        except ValueError:
            pass  # Date format is already validated in _parse_date
        
        # Check cache
        cache_key = self._get_cache_key(origin, destination, parsed_date)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            logger.info("📦 Returning cached flight search result")
            return cached_result
        
        # Call SerpAPI
        try:
            result = await self._call_serpapi(origin, destination, parsed_date)
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in flight search: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Sorry, I encountered an error searching for flights: {str(e)}",
                "tool": "flight_search"
            }
    
    async def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """
        Parse flexible date strings into YYYY-MM-DD format.
        Handles formats like "next Friday", "Dec 15", "this weekend", etc.
        
        Args:
            date_str: Date string (can be flexible)
            
        Returns:
            Date in YYYY-MM-DD format or None if parsing fails
        """
        if not date_str:
            # Default to tomorrow if no date provided
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            return tomorrow
        
        date_str = date_str.strip()
        
        # Try direct parsing first (YYYY-MM-DD, DD-MM-YYYY, etc.)
        try:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    continue
        except:
            pass
        
        # Use Gemini to parse flexible dates if available
        if self.gemini_model:
            try:
                parsed_date = await self._parse_date_with_gemini(date_str)
                if parsed_date:
                    return parsed_date
            except Exception as e:
                logger.warning(f"Gemini date parsing failed: {e}")
        
        # Fallback: try to extract date from common patterns
        # Use IST timezone for accurate date tracking
        today_ist = datetime.now(IST)
        today = today_ist.replace(tzinfo=None)  # For calculations
        
        # Handle relative dates
        date_lower = date_str.lower()
        if "today" in date_lower:
            return today.strftime("%Y-%m-%d")
        elif "tomorrow" in date_lower:
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "next week" in date_lower:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")
        elif "day after tomorrow" in date_lower:
            return (today + timedelta(days=2)).strftime("%Y-%m-%d")
        
        # Handle "next [day of week]" patterns
        import re
        next_day_pattern = r"next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
        match = re.search(next_day_pattern, date_lower)
        if match:
            target_day = match.group(1)
            days_ahead = {
                "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                "friday": 4, "saturday": 5, "sunday": 6
            }
            target_weekday = days_ahead.get(target_day)
            if target_weekday is not None:
                current_weekday = today.weekday()
                days_to_add = (target_weekday - current_weekday) % 7
                if days_to_add == 0:
                    days_to_add = 7  # Next week's day
                return (today + timedelta(days=days_to_add)).strftime("%Y-%m-%d")
        
        # Try to extract month and day from strings like "Dec 15", "December 15", "Dec 3rd"
        month_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2})(?:st|nd|rd|th)?"
        match = re.search(month_pattern, date_lower)
        if match:
            month_name = match.group(1)
            day = int(match.group(2))
            
            month_map = {
                "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
                "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
            }
            
            month = month_map.get(month_name[:3])
            if month:
                year = today.year
                # If month is in the past, assume next year
                if month < today.month or (month == today.month and day < today.day):
                    year += 1
                
                try:
                    parsed = datetime(year, month, day)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    pass
        
        return None
    
    async def _parse_date_with_gemini(self, date_str: str) -> Optional[str]:
        """
        Use Gemini to parse flexible date strings with accurate current date context.
        
        Args:
            date_str: Flexible date string (e.g., "next Friday", "Dec 3rd", "this weekend")
            
        Returns:
            Date in YYYY-MM-DD format or None if parsing fails
        """
        if not self.gemini_model:
            return None
        
        try:
            # Get current date/time in IST (accurate tracking)
            now_ist = datetime.now(IST)
            now_utc = datetime.now(pytz.UTC)
            
            # Build comprehensive date context (like we did for time tracking)
            current_date_info = f"""Current Date and Time Information (CRITICAL - Use this for date parsing):

BASE TIME (India Standard Time - IST):
- Current date: {now_ist.strftime('%B %d, %Y')} ({now_ist.strftime('%Y-%m-%d')})
- Current day of week: {now_ist.strftime('%A')}
- Current month: {now_ist.strftime('%B')} (month {now_ist.month})
- Current year: {now_ist.year}
- Current time: {now_ist.strftime('%I:%M %p IST')}
- Today's date (DD/MM/YYYY): {now_ist.strftime('%d/%m/%Y')}
- UTC time: {now_utc.strftime('%Y-%m-%d %I:%M %p UTC')}

IMPORTANT DATE PARSING RULES:
1. ALWAYS use the current date shown above as reference
2. If year is not mentioned:
   - Use {now_ist.year} if the month/day is >= current date
   - Use {now_ist.year + 1} if the month/day has already passed this year
3. For "next [day of week]", calculate from {now_ist.strftime('%A')} ({now_ist.strftime('%Y-%m-%d')})
4. For "tomorrow", add 1 day to {now_ist.strftime('%Y-%m-%d')}
5. For "this weekend", use the upcoming Saturday
6. For relative dates like "in 3 days", add to {now_ist.strftime('%Y-%m-%d')}
7. Be accurate with month boundaries (e.g., if today is Dec 30, "next Monday" is in next year)

Examples based on today being {now_ist.strftime('%B %d, %Y')}:
- "tomorrow" = {(now_ist + timedelta(days=1)).strftime('%Y-%m-%d')}
- "next week" = {(now_ist + timedelta(days=7)).strftime('%Y-%m-%d')}
- If user says "Dec 10": determine year based on whether Dec 10 has passed
- If user says "next Friday": calculate next Friday from {now_ist.strftime('%A, %B %d')}
"""
            
            prompt = f"""{current_date_info}

Date string to parse: "{date_str}"

Parse this into YYYY-MM-DD format using the current date information provided above.

CRITICAL: Use the exact current date ({now_ist.strftime('%Y-%m-%d')}) shown above for all calculations.

Respond with ONLY the date in YYYY-MM-DD format, nothing else. If you cannot parse it, respond with "null"."""
            
            response = self.gemini_model.generate_content(prompt)
            result = response.text.strip()
            
            # Validate the result
            if result.lower() == "null" or not result:
                return None
            
            # Try to parse the result to ensure it's valid
            try:
                parsed_dt = datetime.strptime(result, "%Y-%m-%d")
                
                # Extra validation: ensure date is not in the past
                today_date = now_ist.date()
                if parsed_dt.date() < today_date:
                    logger.warning(f"Gemini returned past date: {result} (today is {today_date})")
                    # Try to fix: assume they meant next year
                    if parsed_dt.month >= now_ist.month:  # Same or later month, but past year
                        fixed_date = parsed_dt.replace(year=now_ist.year + 1)
                        logger.info(f"Fixed past date to next year: {fixed_date.strftime('%Y-%m-%d')}")
                        return fixed_date.strftime("%Y-%m-%d")
                    return None
                
                return result
            except ValueError:
                logger.warning(f"Gemini returned invalid date format: {result}")
                return None
                
        except Exception as e:
            logger.warning(f"Gemini date parsing error: {e}")
            return None
    
    async def _get_airport_code(self, city_name: str) -> Optional[str]:
        """
        Get airport code (IATA) for a city name using Gemini.
        
        Args:
            city_name: City name (e.g., "Chennai", "Mumbai", "Bagdogra")
            
        Returns:
            Airport code (e.g., "MAA", "BOM", "IXB") or None if not found
        """
        # If it's already a 3-letter uppercase code, return it
        if len(city_name.strip()) == 3 and city_name.strip().isupper():
            return city_name.strip()
        
        # If Gemini is not available, return None
        if not self.gemini_model:
            logger.warning("Gemini not available for airport code conversion")
            return None
        
        try:
            prompt = f"""Convert this city name to its IATA airport code (3-letter uppercase code).

City: "{city_name}"

Examples:
- "Chennai" -> "MAA"
- "Mumbai" -> "BOM"
- "Delhi" -> "DEL"
- "Bagdogra" -> "IXB"
- "New York" -> "JFK"
- "London" -> "LHR"

Respond with ONLY the 3-letter uppercase airport code, nothing else. If you cannot find the airport code, respond with "null"."""
            
            response = self.gemini_model.generate_content(prompt)
            code = response.text.strip().upper()
            
            # Validate it's a 3-letter code
            if len(code) == 3 and code.isalpha():
                logger.info(f"✅ Converted '{city_name}' to airport code: {code}")
                return code
            elif code.lower() == "null":
                logger.warning(f"⚠️  Could not find airport code for '{city_name}'")
                return None
            else:
                # Try to extract 3-letter code from response
                import re
                match = re.search(r'\b([A-Z]{3})\b', code)
                if match:
                    return match.group(1)
                logger.warning(f"⚠️  Invalid airport code format for '{city_name}': {code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting airport code for '{city_name}': {e}")
            return None
    
    async def _call_serpapi(
        self,
        origin: str,
        destination: str,
        date: str
    ) -> Dict[str, Any]:
        """
        Call SerpAPI Google Flights API.
        
        Args:
            origin: Origin city/airport
            destination: Destination city/airport
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dictionary with flight search results
        """
        if not settings.SERPAPI_KEY:
            return {
                "success": False,
                "message": "SerpAPI key not configured. Please set SERPAPI_KEY in environment variables.",
                "tool": "flight_search"
            }
        
        logger.info(f"🔍 Calling SerpAPI: {origin} -> {destination} on {date}")
        
        # SerpAPI Google Flights endpoint
        url = "https://serpapi.com/search"
        
        # Convert city names to airport codes using Gemini
        logger.info(f"🔄 Converting city names to airport codes...")
        logger.info(f"   Origin: '{origin}'")
        origin_code = await self._get_airport_code(origin)
        logger.info(f"   Origin code: {origin_code if origin_code else 'FAILED - using ' + origin.upper()}")
        
        logger.info(f"   Destination: '{destination}'")
        destination_code = await self._get_airport_code(destination)
        logger.info(f"   Destination code: {destination_code if destination_code else 'FAILED - using ' + destination.upper()}")
        
        # If we couldn't get airport codes, use the original (might already be codes)
        departure_id = origin_code if origin_code else origin.upper()
        arrival_id = destination_code if destination_code else destination.upper()
        
        # SerpAPI expects uppercase 3-letter airport codes
        # type=2 for one-way flights, type=1 for round trip (requires return_date)
        params = {
            "engine": "google_flights",
            "api_key": settings.SERPAPI_KEY,
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": date,
            "type": "2",  # 2 = one-way, 1 = round trip
            "currency": "INR",
            "hl": "en",
            "gl": "in"  # India
        }
        
        logger.info(f"✈️ SerpAPI Request: {departure_id} -> {arrival_id} on {date}")
        logger.info(f"📋 Full params: {params}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info(f"📡 Sending request to SerpAPI...")
                response = await client.get(url, params=params)
                
                # Log the request for debugging
                logger.info(f"📡 SerpAPI Status Code: {response.status_code}")
                logger.info(f"📡 SerpAPI request URL: {response.request.url}")
                
                # Check for 400 errors and get detailed error message
                if response.status_code == 400:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("error", "Bad Request")
                        logger.error(f"SerpAPI 400 error: {error_msg}")
                        logger.error(f"Request params: {params}")
                        
                        # Check if we successfully converted to airport codes
                        if origin_code and destination_code:
                            # We used airport codes but still got 400 - route might not exist or date issue
                            return {
                                "success": False,
                                "message": f"I couldn't find flights from {origin} ({departure_id}) to {destination} ({arrival_id}) on {date}. The route might not have flights on that date, or please try a different date.",
                                "tool": "flight_search",
                                "error_type": "invalid_route"
                            }
                        else:
                            # We couldn't convert to airport codes - suggest using codes
                            missing = []
                            if not origin_code:
                                missing.append(f"{origin}")
                            if not destination_code:
                                missing.append(f"{destination}")
                            
                            return {
                                "success": False,
                                "message": f"I couldn't find airport codes for: {', '.join(missing)}. Please try using airport codes directly (e.g., MAA for Chennai, BOM for Mumbai, IXB for Bagdogra).",
                                "tool": "flight_search",
                                "error_type": "invalid_route"
                            }
                    except:
                        return {
                            "success": False,
                            "message": f"I couldn't find flights from {origin} to {destination}. Please check the city names or try using airport codes (e.g., 'MAA' for Chennai, 'IXB' for Bagdogra).",
                            "tool": "flight_search",
                            "error_type": "invalid_route"
                        }
                
                response.raise_for_status()
                data = response.json()
                
                # Check for API errors
                if "error" in data:
                    error_msg = data.get("error", "Unknown error")
                    if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                        return {
                            "success": False,
                            "message": "I've hit my search limit today. Try tomorrow? 😅",
                            "tool": "flight_search",
                            "error_type": "quota_exceeded"
                        }
                    return {
                        "success": False,
                        "message": f"API error: {error_msg}",
                        "tool": "flight_search"
                    }
                
                # Parse and format results
                return self._format_serpapi_results(data, origin, destination, date)
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return {
                    "success": False,
                    "message": "I've hit my search limit today. Try tomorrow? 😅",
                    "tool": "flight_search",
                    "error_type": "quota_exceeded"
                }
            elif e.response.status_code == 400:
                # This shouldn't happen since we handle 400 above, but just in case
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", "Invalid request parameters")
                    logger.error(f"SerpAPI 400 error in exception handler: {error_msg}")
                except:
                    pass
                return {
                    "success": False,
                    "message": f"I couldn't find flights from {origin} to {destination} on {date}. Please check the city names or try using airport codes (e.g., MAA for Chennai, IXB for Bagdogra).",
                    "tool": "flight_search",
                    "error_type": "invalid_request"
                }
            logger.error(f"SerpAPI HTTP error: {e}")
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response text: {e.response.text[:500] if hasattr(e.response, 'text') else 'No response text'}")
            return {
                "success": False,
                "message": f"Failed to search flights: HTTP {e.response.status_code}. Please try again later.",
                "tool": "flight_search"
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "message": "Request timed out. Please try again.",
                "tool": "flight_search"
            }
        except Exception as e:
            logger.error(f"SerpAPI call error: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error searching flights: {str(e)}",
                "tool": "flight_search"
            }
    
    def _format_serpapi_results(
        self,
        data: Dict[str, Any],
        origin: str,
        destination: str,
        date: str
    ) -> Dict[str, Any]:
        """
        Format SerpAPI results for WhatsApp display.
        
        Args:
            data: Raw SerpAPI response
            origin: Origin city
            destination: Destination city
            date: Travel date
            
        Returns:
            Formatted result dictionary
        """
        try:
            logger.info(f"🔧 Formatting SerpAPI results...")
            logger.info(f"📋 Response keys: {list(data.keys())}")
            
            # Extract best flights from SerpAPI response
            # SerpAPI structure may vary, so we'll handle multiple possible structures
            flights = []
            
            # Try to extract flights from different possible response structures
            if "best_flights" in data:
                logger.info(f"✅ Found 'best_flights' in response with {len(data['best_flights'])} flights")
                flights_data = data["best_flights"]
            elif "flights" in data:
                flights_data = data["flights"]
            elif "other_flights" in data:
                flights_data = data["other_flights"]
            else:
                # Try to find any flight-like structure
                flights_data = []
                for key in data.keys():
                    if "flight" in key.lower() and isinstance(data[key], list):
                        flights_data = data[key]
                        break
            
            if not flights_data:
                return {
                    "success": False,
                    "message": "No flights found for those dates. Try different dates?",
                    "tool": "flight_search"
                }
            
            # Extract top 3 cheapest flights
            for flight_item in flights_data[:3]:
                try:
                    flight_info = self._extract_flight_info(flight_item)
                    if flight_info:
                        flights.append(flight_info)
                except Exception as e:
                    logger.warning(f"Error extracting flight info: {e}")
                    continue
            
            if not flights:
                return {
                    "success": False,
                    "message": "No flights found for those dates. Try different dates?",
                    "tool": "flight_search"
                }
            
            # Format date for display
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                date_display = date_obj.strftime("%b %d, %Y")
            except:
                date_display = date
            
            return {
                "success": True,
                "flights": flights,
                "origin": origin,
                "destination": destination,
                "date": date_display,
                "count": len(flights),
                "tool": "flight_search"
            }
            
        except Exception as e:
            logger.error(f"Error formatting SerpAPI results: {e}", exc_info=True)
            return {
                "success": False,
                "message": "I found flights but had trouble formatting them. Please try again.",
                "tool": "flight_search"
            }
    
    def _extract_flight_info(self, flight_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract flight information from SerpAPI flight item.
        
        Args:
            flight_item: Single flight item from SerpAPI response
            
        Returns:
            Dictionary with flight info or None
        """
        try:
            # SerpAPI structure can vary, so we'll try multiple paths
            price = None
            airline = "Unknown"
            departure_time = None
            arrival_time = None
            stops = "Direct"
            booking_link = None
            
            # Extract price
            if "price" in flight_item:
                price_data = flight_item["price"]
                if isinstance(price_data, dict):
                    price = price_data.get("total", price_data.get("price"))
                else:
                    price = price_data
            
            # Extract airline
            if "airline" in flight_item:
                airline_data = flight_item["airline"]
                if isinstance(airline_data, dict):
                    airline = airline_data.get("name", airline_data.get("title", "Unknown"))
                else:
                    airline = str(airline_data)
            
            # Extract times
            if "departure_airport" in flight_item:
                dep_data = flight_item["departure_airport"]
                if isinstance(dep_data, dict):
                    departure_time = dep_data.get("time", dep_data.get("datetime"))
            
            if "arrival_airport" in flight_item:
                arr_data = flight_item["arrival_airport"]
                if isinstance(arr_data, dict):
                    arrival_time = arr_data.get("time", arr_data.get("datetime"))
            
            # Extract stops
            if "stops" in flight_item:
                stops_data = flight_item["stops"]
                if stops_data and stops_data > 0:
                    stops = f"{stops_data} stop(s)"
            
            # Extract booking link
            if "links" in flight_item:
                links = flight_item["links"]
                if isinstance(links, list) and links:
                    booking_link = links[0].get("link") if isinstance(links[0], dict) else links[0]
            elif "link" in flight_item:
                booking_link = flight_item["link"]
            
            # Format price in INR
            if price:
                if isinstance(price, str):
                    # Remove currency symbols and convert
                    price_clean = price.replace("₹", "").replace(",", "").replace(",", "").strip()
                    try:
                        price = float(price_clean)
                    except:
                        pass
                
                if isinstance(price, (int, float)):
                    price_formatted = f"₹{price:,.0f}"
                else:
                    price_formatted = str(price)
            else:
                price_formatted = "Price not available"
            
            return {
                "airline": airline,
                "price": price_formatted,
                "price_numeric": price if isinstance(price, (int, float)) else None,
                "departure_time": departure_time or "N/A",
                "arrival_time": arrival_time or "N/A",
                "stops": stops,
                "booking_link": booking_link
            }
            
        except Exception as e:
            logger.warning(f"Error extracting flight info: {e}")
            return None
    
    def _get_cache_key(self, origin: str, destination: str, date: str) -> str:
        """Generate cache key for search parameters."""
        return f"{origin.lower()}_{destination.lower()}_{date}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired."""
        if cache_key not in self.cache:
            return None
        
        cached = self.cache[cache_key]
        cached_time = cached.get("timestamp")
        
        if not cached_time:
            return None
        
        try:
            cached_datetime = datetime.fromisoformat(cached_time)
            if datetime.now() - cached_datetime > self.CACHE_DURATION:
                # Cache expired
                del self.cache[cache_key]
                return None
            
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached.get("result")
        except Exception as e:
            logger.warning(f"Error checking cache: {e}")
            return None
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]) -> None:
        """Cache search result."""
        self.cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        logger.debug(f"Cached result for key: {cache_key}")
