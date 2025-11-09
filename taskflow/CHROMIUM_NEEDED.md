# Do You Need Chromium?

## Short Answer

**NO, you don't need Chromium if you're not using price tracking.**

Chromium is **ONLY** needed for the **Price Tracking** feature. All other features work without it!

## Feature Breakdown

| Feature           | Needs Chromium? | What It Uses                         |
| ----------------- | --------------- | ------------------------------------ |
| ✈️ Flight Search  | ❌ NO           | SerpAPI (HTTP requests)              |
| ⏰ Reminders      | ❌ NO           | Python datetime parsing              |
| 💬 General Chat   | ❌ NO           | Gemini API                           |
| 📦 Price Tracking | ✅ YES          | Playwright + Chromium (web scraping) |

## Why Tests Might Pass Without Chromium

The `test_features.py` script only checks if:

- The webhook endpoint returns HTTP 200 (success)
- The server processes the request

It doesn't check if the actual feature works!

**Without Chromium:**

- ✅ Webhook returns 200 (test passes)
- ✅ Server processes the request
- ❌ Price tracking returns error: "Price tracking requires Playwright"
- ✅ Other features work perfectly

## How to Check If You Need Chromium

Run this check script:

```bash
cd taskflow
source venv/bin/activate
python3 check_chromium_needed.py
```

## When to Install Chromium

**Install Chromium ONLY if:**

1. You want to use price tracking
2. You want to scrape Amazon product prices
3. You want to track product prices over time

**Don't install if:**

- You only use flight search
- You only use reminders
- You only use general chat
- You're just testing the system

## Chromium Size

- **Size:** ~170MB
- **Location:** `~/Library/Caches/ms-playwright/`
- **Can be deleted:** Yes, anytime with `playwright uninstall chromium`

## Test Without Chromium

You can test all features except price tracking:

```bash
# These work WITHOUT Chromium:
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=flights from Delhi to Mumbai tomorrow"

curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Remind me to call doctor tomorrow at 3pm"

# This will return an error WITHOUT Chromium:
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Track iPhone price on Amazon"
```

## Install Chromium (Only If Needed)

If you decide you need price tracking:

```bash
cd taskflow
source venv/bin/activate
playwright install chromium
```

This downloads ~170MB to `~/Library/Caches/ms-playwright/`

## Summary

- **75% of features work without Chromium** (flights, reminders, chat)
- **Only price tracking needs Chromium**
- **Tests might pass, but price tracking won't work without it**
- **Install only if you need price tracking**
