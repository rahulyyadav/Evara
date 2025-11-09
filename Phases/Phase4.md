Implement price tracking using web scraping (Playwright).

File: tools/price_tracker.py

This tool should:

1. Take product URL or search query
2. If search query: find product on Amazon/Flipkart
3. Scrape current price
4. Save to memory with user's phone number
5. Check daily and alert on price drop

Supported Sites (Start with Amazon India):

- Amazon.in
- Flipkart.com (optional for v1)

Features:

1. Track new product: Extract title, current price, URL, image
2. Check tracked products: Show all items user is tracking
3. Daily price check: Background job (simulate with manual trigger for v1)
4. Alert on drop: Send WhatsApp message when price drops

Key Requirements:

- Use Playwright in headless mode
- Handle dynamic loading (wait for price element)
- Parse price correctly (handle ₹, commas, decimals)
- Store tracking data in user_memory.json
- Handle "out of stock" gracefully

Error Handling:

- Invalid URL → "I couldn't access that page. Check the URL?"
- Product not found → "Couldn't find that product. Send me the direct link?"
- Scraping blocked → "Website blocked me. Try with a different product?"

User Commands:

- "Track iPhone 15 price on Amazon" → Search and track
- "Check tracked items" → Show all tracking
- "Stop tracking [product]" → Remove from tracking

Response Format:
"📦 Tracking: iPhone 15 (128GB)
💰 Current: ₹69,999
📉 I'll alert you if price drops below ₹65,000

You're tracking 2 items total."

Implement with:

1. PriceTrackerTool class
2. track_product() async method
3. check_prices() to scan all tracked items
4. \_scrape_amazon() using Playwright
5. \_parse_price() to extract numeric value
6. Store in memory with structure:
   {
   "user_number": {
   "tracked_products": [
   {
   "id": "uuid",
   "title": "iPhone 15",
   "url": "...",
   "current_price": 69999,
   "target_price": 65000,
   "tracked_since": "2025-11-06"
   }
   ]
   }
   }
