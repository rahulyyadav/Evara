# TaskFlow Testing Guide

This guide explains how to test all features of TaskFlow locally.

## Prerequisites

1. **Install Dependencies**

   ```bash
   cd taskflow
   source venv/bin/activate
   pip install -r requirements.txt

   # Install Playwright browsers (for price tracking)
   playwright install chromium
   ```

2. **Set Up Environment Variables**
   Create a `.env` file in the `taskflow` directory:

   ```env
   # Required
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

   # Optional but recommended
   GEMINI_API_KEY=your_gemini_api_key
   SERPAPI_KEY=your_serpapi_key

   # Server settings
   ENVIRONMENT=development
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```

## Starting the Server

```bash
cd taskflow
source venv/bin/activate
python3 -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

## Testing Methods

### Method 1: Using the Test Script (Recommended)

I'll create a test script that simulates WhatsApp messages.

### Method 2: Using curl/Postman

Send POST requests to the webhook endpoint to simulate incoming messages.

### Method 3: Using FastAPI Docs

Visit `http://localhost:8000/docs` for interactive API documentation.

## Testing Each Feature

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "app": "TaskFlow",
  "version": "1.0.0",
  "environment": "development",
  "twilio_configured": true
}
```

### 2. Flight Search

**Test Message:**

```
"flights from Delhi to Mumbai on Dec 15"
```

**Using curl:**

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=flights from Delhi to Mumbai on Dec 15" \
  -d "MessageSid=test001"
```

**Expected Response:**

- If SerpAPI is configured: Flight search results with top 3 options
- If not configured: Error message about missing API key

### 3. Price Tracking

**Test Messages:**

```
"Track iPhone 15 price on Amazon"
"Check tracked items"
"Stop tracking iPhone"
```

**Using curl:**

```bash
# Track a product
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Track iPhone 15 price on Amazon" \
  -d "MessageSid=test002"

# Check tracked items
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Check tracked items" \
  -d "MessageSid=test003"
```

**Expected Response:**

- Product tracking confirmation with current price
- List of all tracked items

### 4. Reminders

**Test Messages:**

```
"Remind me to call doctor tomorrow at 3pm"
"Show my reminders"
"Cancel reminder 1"
```

**Using curl:**

```bash
# Set a reminder
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Remind me to call doctor tomorrow at 3pm" \
  -d "MessageSid=test004"

# List reminders
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Show my reminders" \
  -d "MessageSid=test005"
```

**Expected Response:**

- Reminder confirmation with date/time
- List of active reminders

### 5. General Chat

**Test Messages:**

```
"Hello"
"What can you do?"
"Help"
```

**Expected Response:**

- Friendly greeting and feature overview

## Testing Reminder Background Job

The reminder checker runs every minute. To test:

1. Set a reminder for 1-2 minutes in the future:

   ```
   "Remind me to test in 2 minutes"
   ```

2. Wait and check logs - you should see:

   ```
   ✅ Sent reminder to [user_number]: test
   ```

3. Check the memory file (`data/user_memory.json`) - reminder status should be "sent"

## Testing Without Twilio WhatsApp

Since you don't have a Twilio WhatsApp number yet, the app will:

- Accept incoming webhook requests (signature validation is skipped in development mode)
- Process messages and generate responses
- **But fail to send responses back** (since there's no valid WhatsApp number)

To see the responses:

1. Check the server logs - responses are logged
2. The response is generated but sending fails (this is expected)

## Checking Logs

All actions are logged. Watch the console output for:

- ✅ Success messages
- ❌ Error messages
- 📊 Intent classification
- 🔧 Tool execution
- 📤 Message sending attempts

## Testing Checklist

- [ ] Server starts without errors
- [ ] Health check endpoint works
- [ ] Flight search (if SerpAPI key set)
- [ ] Price tracking (if Playwright installed)
- [ ] Reminder creation
- [ ] Reminder listing
- [ ] Reminder cancellation
- [ ] Background reminder checker running
- [ ] Memory persistence (check `data/user_memory.json`)

## Common Issues

1. **ModuleNotFoundError**: Install missing packages with `pip install -r requirements.txt`
2. **Playwright not installed**: Run `playwright install chromium`
3. **API keys missing**: Features will work with fallback responses
4. **Port already in use**: Change PORT in `.env` or kill the process using port 8000

## Next Steps

Once you have a Twilio WhatsApp number:

1. Update `TWILIO_WHATSAPP_NUMBER` in `.env`
2. Configure webhook URL in Twilio dashboard
3. Test with real WhatsApp messages
