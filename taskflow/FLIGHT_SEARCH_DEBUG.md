# ✈️ Flight Search Debugging Guide

## Current Implementation

### Flow:

1. **User Request** → `agent.py` classifies intent
2. **Extract entities** → origin, destination, date
3. **FlightSearchTool.search()** →
   - Validates inputs
   - Parses date using Gemini
   - Converts city names to airport codes using Gemini
   - Calls SerpAPI Google Flights
   - Parses and formats results

### Dependencies:

- ✅ SerpAPI key (SERPAPI_KEY)
- ✅ Gemini API (for date parsing & airport codes)

## Common Issues & Fixes

### Issue 1: "Flight search not working"

**Symptoms:** Agent doesn't find flights or returns error

**Possible causes:**

1. SERPAPI_KEY not set
2. Gemini can't convert city names
3. Date parsing fails
4. Invalid route (no flights exist)

**Debug steps:**

1. Check Render logs for:

   ```
   ✈️ Flight search: chennai -> bangalore on dec 15
   🔍 Calling SerpAPI: chennai -> bangalore on 2025-12-15
   Using airport codes: MAA -> BLR
   ```

2. Look for errors:
   ```
   ❌ SerpAPI 400 error: invalid_route
   ⚠️  Could not find airport code for 'XXX'
   ```

### Issue 2: Wrong dates

**Symptoms:** Searches for past dates or wrong month

**Fix:** Already implemented timezone-aware date parsing in IST

### Issue 3: Can't convert city names

**Symptoms:** "I couldn't find airport codes"

**Solution:** Use airport codes directly:

- Chennai = MAA
- Mumbai = BOM
- Delhi = DEL
- Bangalore = BLR
- Bagdogra = IXB

### Issue 4: SerpAPI returns no results

**Symptoms:** "I couldn't find any flights"

**Causes:**

- Route doesn't exist
- No flights on that date
- SerpAPI credit exhausted

## Testing Flight Search

### Test 1: Basic search

```
search flights from chennai to bangalore on dec 15
```

Expected:

- ✅ Converts "chennai" → "MAA", "bangalore" → "BLR"
- ✅ Parses "dec 15" → "2025-12-15"
- ✅ Calls SerpAPI
- ✅ Returns flight results

### Test 2: With airport codes

```
search flights from MAA to BLR on dec 15
```

Expected:

- ✅ Skips conversion (already codes)
- ✅ Direct SerpAPI call
- ✅ Returns results

### Test 3: Flexible dates

```
search flights from chennai to mumbai next friday
```

Expected:

- ✅ Gemini parses "next friday" to date
- ✅ Converts cities to codes
- ✅ Returns results

## Debug Endpoint

Check if SerpAPI is configured:

```
https://evara-8w6h.onrender.com/health
```

Look for:

```json
{
  "api_keys": {
    "serpapi_configured": true  ← Should be true
  }
}
```

## Logs to Check

After flight search request, check Render logs for:

1. **Intent classification:**

   ```
   📊 Intent: flight_search
   📋 Entities: {origin: "chennai", destination: "bangalore", date: "dec 15"}
   ```

2. **Tool execution:**

   ```
   ✈️ Flight search: chennai -> bangalore on dec 15
   ```

3. **Date parsing:**

   ```
   Parsed date: dec 15 → 2025-12-15
   ```

4. **Airport code conversion:**

   ```
   ✅ Converted 'chennai' to airport code: MAA
   ✅ Converted 'bangalore' to airport code: BLR
   ```

5. **SerpAPI call:**

   ```
   🔍 Calling SerpAPI: chennai -> bangalore on 2025-12-15
   Using airport codes: MAA -> BLR
   ```

6. **Results:**
   ```
   ✅ Found X flight(s) from MAA to BLR
   ```

## Common Errors

### Error 1: "SerpAPI key not configured"

**Fix:** Add SERPAPI_KEY to .env on Render

### Error 2: "I couldn't find airport codes"

**Fix:** Gemini failed. Tell user to use codes (MAA, BOM, etc.)

### Error 3: "I couldn't find any flights"

**Causes:**

- No flights on that route/date
- SerpAPI returned empty results
- Invalid date (past date)

### Error 4: "Error searching for flights: timeout"

**Fix:** SerpAPI slow/down. Increase timeout or retry

## What to Share for Debugging

1. **WhatsApp message you sent**
2. **Agent's response**
3. **Output of `/health` endpoint**
4. **Render logs** (search for "✈️" or "flight")

## Quick Fixes

### Fix 1: If date parsing broken

Already fixed with IST timezone awareness

### Fix 2: If airport codes not converting

Fallback already implemented - uses city name uppercase

### Fix 3: If SerpAPI failing

Check:

- SerpAPI credit balance
- API key is correct
- Network connectivity

## API Keys Check

Required environment variables on Render:

```bash
SERPAPI_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```

To verify:

```bash
# Check health endpoint
curl https://evara-8w6h.onrender.com/health | jq '.api_keys'
```

Expected:

```json
{
  "gemini_configured": true,
  "serpapi_configured": true
}
```

---

**Ready to debug!** Share what happens when you test flight search.
