# TaskFlow Quick Start Guide 🚀

Get TaskFlow up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.11+)
python3 --version

# Check pip
pip3 --version

# Check git
git --version
```

## 1. Setup (30 seconds)

```bash
cd taskflow
./setup.sh
```

This automatically:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Creates data and logs directories
- ✅ Copies .env.example to .env

## 2. Configure Twilio (2 minutes)

### Get Credentials

1. Sign up at [Twilio](https://www.twilio.com/try-twilio) (free)
2. Go to [Console](https://console.twilio.com/)
3. Copy **Account SID** and **Auth Token**
4. Go to [WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
5. Note your sandbox number

### Update .env

Edit `taskflow/.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## 3. Run Locally (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
python -m app.main
```

You should see:
```
🚀 Starting TaskFlow application...
✅ Twilio client initialized successfully
✅ TaskFlow is ready to receive messages!
```

## 4. Expose to Internet (1 minute)

In a new terminal:
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

## 5. Connect Twilio (30 seconds)

1. Open [WhatsApp Sandbox Settings](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
2. Set "WHEN A MESSAGE COMES IN" to: `https://abc123.ngrok.io/webhook`
3. Method: `HTTP POST`
4. Click **Save**

## 6. Test! 🎉

1. Send join code to Twilio sandbox number (shown in Twilio console)
2. Send "Hello!" to the bot
3. You should get a response!

## Verify Everything Works

### Check Server Health
```bash
curl http://localhost:8000/health
```

### Check Logs
```bash
tail -f logs/taskflow.log
```

### Test Message Flow
Send a WhatsApp message and watch the logs!

## Common Issues

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 8000 in use"
```bash
# Use different port
PORT=8001 python -m app.main
```

### "Signature validation failed"
```bash
# For local testing, add to .env:
DEBUG=True
```

### Messages not received
- ✅ Check server is running
- ✅ Check ngrok is running
- ✅ Check webhook URL in Twilio
- ✅ Check you've joined the sandbox

## What's Next?

### Test Different Messages
- Short messages
- Long messages
- Emojis 🚀
- Questions

### View Logs
```bash
# Follow logs in real-time
tail -f logs/taskflow.log

# Search logs
grep "ERROR" logs/taskflow.log
```

### Check Twilio Debugger
[Twilio Debugger](https://console.twilio.com/monitor/debugger) shows all API calls

### Prepare for Phase 2
- Get [Gemini API key](https://makersuite.google.com/app/apikey)
- Review Phase 2 documentation
- Think about tasks you want to automate!

## Useful Commands

```bash
# Start server
python -m app.main

# Start with custom port
PORT=8001 python -m app.main

# Check health
curl http://localhost:8000/health

# Test webhook
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Test message"

# View logs
tail -f logs/taskflow.log

# Check running processes
ps aux | grep python

# Stop server
# Press Ctrl+C in terminal
```

## Success Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env configured with Twilio credentials
- [ ] Server running (http://localhost:8000)
- [ ] Ngrok exposing server
- [ ] Twilio webhook configured
- [ ] Joined WhatsApp sandbox
- [ ] Successfully sent and received a message
- [ ] Logs showing activity

## Need Help?

1. **Check the logs:** `tail -f logs/taskflow.log`
2. **Check Twilio debugger:** [console.twilio.com/monitor/debugger](https://console.twilio.com/monitor/debugger)
3. **Test health endpoint:** `curl http://localhost:8000/health`
4. **Review setup guide:** See `docs/setup-guide.md`

## Ready for Production?

See `README.md` for deployment instructions to Render, Heroku, or other platforms.

---

**Congratulations! Your WhatsApp AI agent is live! 🎉**

Send it a message and watch the magic happen! ✨

