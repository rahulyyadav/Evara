# 🧪 Local Testing Guide for TaskFlow Agent

This guide shows you how to test your WhatsApp agent locally, just like testing a fullstack app on localhost.

## Quick Start

### 1. Start the Server

```bash
cd taskflow
source venv/bin/activate
python3 -m app.main
```

The server will start at `http://localhost:8000`

### 2. Test Endpoints Directly

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Root Endpoint
```bash
curl http://localhost:8000/
```

#### Interactive API Documentation
Open in your browser:
```
http://localhost:8000/docs
```

This gives you a Swagger UI where you can test all endpoints interactively!

### 3. Test Webhook (Simulate WhatsApp Messages)

Since you're in development mode, signature validation is skipped. You can simulate WhatsApp messages:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello TaskFlow!" \
  -d "MessageSid=test123" \
  -d "NumMedia=0"
```

### 4. Use the Test Script

I've created a test script for you:

```bash
cd taskflow
./test_agent.sh
```

This script will:
- ✅ Check if server is running
- ✅ Test health endpoint
- ✅ Test root endpoint
- ✅ Test webhook with multiple messages
- ✅ Show recent logs

## Testing Workflow (Like Fullstack App)

### Step 1: Start Server
```bash
cd taskflow
source venv/bin/activate
python3 -m app.main
```

### Step 2: Test in Another Terminal

**Option A: Use the test script**
```bash
cd taskflow
./test_agent.sh
```

**Option B: Manual testing**
```bash
# Health check
curl http://localhost:8000/health

# Test webhook
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Test message"
```

**Option C: Use browser**
- Open: http://localhost:8000/docs
- Click "Try it out" on any endpoint
- Test interactively!

### Step 3: Watch Logs
```bash
tail -f taskflow/logs/taskflow.log
```

## Testing Different Scenarios

### Test Short Messages
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hi" \
  -d "MessageSid=test001"
```

### Test Long Messages
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=This is a very long message to test how the agent handles longer text content with multiple sentences and words." \
  -d "MessageSid=test002"
```

### Test Messages with Emojis
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello! 🚀 How are you? 😊" \
  -d "MessageSid=test003"
```

## Development Mode Settings

Your `.env` should have:
```bash
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

This enables:
- ✅ Signature validation bypass (for local testing)
- ✅ Detailed logging
- ✅ Auto-reload on code changes

## Monitoring

### View Logs in Real-Time
```bash
tail -f taskflow/logs/taskflow.log
```

### Search Logs
```bash
grep "ERROR" taskflow/logs/taskflow.log
grep "Incoming WhatsApp message" taskflow/logs/taskflow.log
```

### Check Server Status
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

## Testing with Real WhatsApp (Optional)

If you want to test with actual WhatsApp messages:

1. **Expose your local server:**
   ```bash
   ngrok http 8000
   ```

2. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

3. **Update Twilio webhook:**
   - Go to [Twilio WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
   - Set webhook URL to: `https://abc123.ngrok.io/webhook`
   - Method: `HTTP POST`

4. **Send a WhatsApp message** to your Twilio number

## Common Commands

```bash
# Start server
cd taskflow && source venv/bin/activate && python3 -m app.main

# Test health
curl http://localhost:8000/health

# Test webhook
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Test"

# Run test script
./test_agent.sh

# Watch logs
tail -f logs/taskflow.log

# Stop server
# Press Ctrl+C in the terminal running the server
```

## Troubleshooting

### Server won't start
- Check if port 8000 is in use: `lsof -i :8000`
- Use different port: `PORT=8001 python3 -m app.main`

### Module not found
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Webhook returns 403
- Check `.env` has `DEBUG=True` and `ENVIRONMENT=development`
- This bypasses signature validation in dev mode

## Next Steps

1. ✅ Test basic endpoints
2. ✅ Test webhook with different messages
3. ✅ Watch logs to see agent processing
4. 🚀 Add AI capabilities (Phase 2)
5. 🚀 Test with real WhatsApp (optional)

---

**Happy Testing! 🎉**

