"""
Flight search tool for TaskFlow.
Uses SerpAPI to search for flights and return results.
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

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
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }
                )
                logger.debug("Gemini model initialized for flight search")
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
        if not origin or not destination:
            missing = []
            if not origin:
                missing.append("origin city")
            if not destination:
                missing.append("destination city")
            
            return {
                "success": False,
                "needs_clarification": True,
                "message": f"I need more information to search flights. Please provide: {', '.join(missing)}.",
                "tool": "flight_search"
            }
        
        # Parse and normalize date
        parsed_date = await self._parse_date(date)
        if not parsed_date:
            return {
                "success": False,
                "needs_clarification": True,
                "message": "I couldn't understand the date. Please specify a date like 'Dec 15', 'next Friday', or '2024-12-15'.",
                "tool": "flight_search"
            }
        
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
        today = datetime.now()
        
        # Handle relative dates
        date_lower = date_str.lower()
        if "today" in date_lower:
            return today.strftime("%Y-%m-%d")
        elif "tomorrow" in date_lower:
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "next week" in date_lower:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Try to extract month and day from strings like "Dec 15", "December 15"
        import re
        month_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2})"
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
        Use Gemini to parse flexible date strings.
        
        Args:
            date_str: Flexible date string
            
        Returns:
            Date in YYYY-MM-DD format or None
        """
        if not self.gemini_model:
            return None
        
        prompt = f"""Parse this date string into YYYY-MM-DD format. Today is {datetime.now().strftime("%Y-%m-%d")}.

Date string: "{date_str}"

Respond with ONLY the date in YYYY-MM-DD format, nothing else. If you cannot parse it, respond with "null"."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result = response.text.strip()
            
            if result.lower() == "null" or not result:
                return None
            
            # Validate the date format
            try:
                datetime.strptime(result, "%Y-%m-%d")
                return result
            except ValueError:
                return None
                
        except Exception as e:
            logger.warning(f"Gemini date parsing error: {e}")
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
        
        # SerpAPI expects airport codes or city names
        # We'll use the origin/destination as-is (they might be city names or codes)
        params = {
            "engine": "google_flights",
            "api_key": settings.SERPAPI_KEY,
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": date,
            "currency": "INR",
            "hl": "en",
            "gl": "in",  # India
            "type": 1  # One-way flight
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
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
            logger.error(f"SerpAPI HTTP error: {e}")
            return {
                "success": False,
                "message": f"Failed to search flights: HTTP {e.response.status_code}",
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
            # Extract best flights from SerpAPI response
            # SerpAPI structure may vary, so we'll handle multiple possible structures
            flights = []
            
            # Try to extract flights from different possible response structures
            if "best_flights" in data:
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
