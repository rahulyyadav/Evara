Implement the flight search tool using SerpAPI (free tier: 100 searches/month).

File: tools/flight_search.py

This tool should:

1. Take user query like "flights from Delhi to Mumbai on Dec 15"
2. Extract: origin, destination, date using Gemini
3. Use SerpAPI Google Flights API to get real flight data
4. Return top 3 cheapest options with:
   - Airline name
   - Departure/arrival times
   - Price
   - Direct/stops
   - Booking link

Key Requirements:

- Handle flexible date searches ("next Friday", "this weekend")
- Handle missing information (ask user: "Which date?" or "From which city?")
- Cache results for 1 hour to save API calls
- Format prices in INR
- Handle API errors gracefully (quota exceeded, no results found)

Error Handling:

- SerpAPI quota exceeded → "I've hit my search limit today. Try tomorrow?"
- No flights found → "No flights found for those dates. Try different dates?"
- Invalid location → "I couldn't find that city. Can you be more specific?"

Response Format Example:
"Found 3 flights from Delhi to Mumbai on Dec 15:

✈️ IndiGo - ₹4,250
⏰ 08:30 - 10:45 (Direct)
🔗 [Book here]

✈️ Air India - ₹4,890  
⏰ 14:20 - 16:35 (Direct)
🔗 [Book here]

✈️ SpiceJet - ₹3,950
⏰ 22:15 - 00:30+1 (Direct)  
🔗 [Book here]

Want me to check baggage options or flexible dates?"

Implement with:

1. FlightSearchTool class
2. search() async method
3. \_extract_params() using Gemini
4. \_call_serpapi() with retry logic
5. \_format_results() for WhatsApp
6. Basic caching (in-memory dict)
