# ✈️ Flight Search - How It Works

## YES! You can use city names! 🎉

You **DO NOT** need to use airport codes. The agent automatically converts city names to airport codes using Gemini AI.

## Examples

### ✅ Both work the same way:

**Option 1: City Names (Recommended)**
```
"Search flight from Chennai to Bagdogra on 2nd Dec"
"Find flights Chennai to Bagdogra Dec 2"
"Flights from Chennai to Bagdogra on Dec 2nd"
```

**Option 2: Airport Codes (Also works)**
```
"Search flight from MAA to IXB on 2nd Dec"
```

### What Happens Behind the Scenes

When you say: **"Chennai to Bagdogra"**

1. Agent receives: `origin="Chennai"`, `destination="Bagdogra"`
2. Gemini converts:
   - Chennai → MAA (Chennai International Airport)
   - Bagdogra → IXB (Bagdogra Airport)
3. SerpAPI searches: MAA → IXB
4. Returns: Flight prices and options

## More Examples

### Domestic Flights (India)
```
✅ "Flights from Mumbai to Delhi tomorrow"
   → Converts: BOM → DEL

✅ "Search tickets Bangalore to Kolkata next Friday"
   → Converts: BLR → CCU

✅ "Find flights Hyderabad to Chennai Dec 15"
   → Converts: HYD → MAA
```

### International Flights
```
✅ "Flights from Delhi to Dubai next week"
   → Converts: DEL → DXB

✅ "Find tickets Mumbai to London Dec 20"
   → Converts: BOM → LHR

✅ "Search flights Chennai to Singapore tomorrow"
   → Converts: MAA → SIN
```

### Flexible Formats Accepted
```
✅ "Chennai to Bagdogra"
✅ "from Chennai to Bagdogra"
✅ "Chennai Bagdogra"
✅ "MAA to IXB" (codes also work)
✅ "Chennai → Bagdogra"
```

## What You Get Back

```
✈️ Flight Search Results
📍 Chennai (MAA) → Bagdogra (IXB)
📅 December 2, 2024

Found 3 flight(s):

1. IndiGo
   💰 ₹4,500
   ⏰ 10:30 AM → 12:45 PM
   🛫 Direct

2. Air India
   💰 ₹5,200
   ⏰ 2:15 PM → 4:30 PM
   🛫 Direct

3. SpiceJet
   💰 ₹4,800
   ⏰ 6:00 PM → 8:15 PM
   🛫 Direct
```

## Error Handling

If city name can't be converted:
```
"I couldn't find the airport code for [city name]. 
Please try the 3-letter airport code (e.g., DEL for Delhi)"
```

If no flights found:
```
"I couldn't find flights from Chennai (MAA) to Bagdogra (IXB) on Dec 2. 
Try a different date?"
```

## Pro Tips

✅ **Use city names** - Easier and more natural
✅ **Flexible dates** - "tomorrow", "next Friday", "Dec 15"
✅ **Any order** - "flights to Mumbai from Chennai" works too
✅ **Airport codes optional** - Only if you know them

---

**Bottom line**: Just talk naturally! Say "Chennai to Bagdogra" and the agent handles everything. 🚀
