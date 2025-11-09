# TaskFlow Setup Guide

Complete guide for setting up TaskFlow from scratch.

## Prerequisites

### Required
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Twilio Account** - [Sign up](https://www.twilio.com/try-twilio) (free)
- **Git** - [Download](https://git-scm.com/downloads)

### Optional (for future phases)
- **Google Gemini API Key** - [Get key](https://makersuite.google.com/app/apikey)
- **SerpAPI Key** - [Sign up](https://serpapi.com/)

## Quick Setup (Recommended)

### 1. Run the Setup Script

```bash
cd taskflow
./setup.sh
```

This script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create necessary directories
- ✅ Copy .env.example to .env

### 2. Configure Twilio

#### Get Twilio Credentials
1. Go to [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token**
3. Go to [WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
4. Note your sandbox number (e.g., `whatsapp:+14155238886`)

#### Update .env File
Edit `taskflow/.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 3. Run the Application

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the app
python -m app.main
```

You should see:
```
🚀 Starting TaskFlow application...
Environment: development
✅ Twilio client initialized successfully
✅ TaskFlow is ready to receive messages!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Expose Local Server (for Testing)

Use ngrok or a similar tool:
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 5. Configure Twilio Webhook

1. Go to [Twilio WhatsApp Sandbox Settings](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
2. Under "WHEN A MESSAGE COMES IN":
   - URL: `https://abc123.ngrok.io/webhook`
   - Method: `HTTP POST`
3. Click **Save**

### 6. Test It!

1. Send the join code to your Twilio sandbox number (shown in Twilio console)
2. Send any message to the bot
3. You should receive a response!

## Manual Setup

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
cd taskflow
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create Directories

```bash
mkdir -p data logs
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Run Application

```bash
python -m app.main
```

## Verification Steps

### Check Application Health

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

### Test Webhook Locally

```bash
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello TaskFlow!" \
  -d "MessageSid=test123"
```

### Check Logs

```bash
tail -f logs/taskflow.log
```

## Production Deployment

### Deploy to Render

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Phase 1"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   
3. **Configure Build Settings**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** 
     ```bash
     gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```

4. **Add Environment Variables**
   ```
   ENVIRONMENT=production
   DEBUG=False
   TWILIO_ACCOUNT_SID=your_actual_sid
   TWILIO_AUTH_TOKEN=your_actual_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   LOG_LEVEL=INFO
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

6. **Update Twilio Webhook**
   - Copy your Render URL (e.g., `https://taskflow-abc.onrender.com`)
   - Update Twilio webhook to: `https://taskflow-abc.onrender.com/webhook`

### Deploy to Other Platforms

#### Heroku
```bash
# Add Procfile
echo "web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:\$PORT" > Procfile

# Deploy
heroku create taskflow-yourname
git push heroku main
heroku config:set TWILIO_ACCOUNT_SID=your_sid
# ... set other env vars
```

#### Railway
- Connect GitHub repository
- Railway auto-detects Python
- Add environment variables in dashboard
- Deploy automatically on push

#### DigitalOcean App Platform
- Similar to Render
- Connect repository
- Configure build/start commands
- Add environment variables

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Twilio signature validation failed"

**Solution:**
- Ensure webhook URL in Twilio exactly matches your server URL
- Include `https://` and no trailing slash unless your URL has one
- For local dev, set `DEBUG=True` in `.env` to skip validation

### Issue: "Messages not being received"

**Solution:**
1. Check server is running: `curl http://localhost:8000/health`
2. Check Twilio sandbox is active
3. Verify you've joined the sandbox (send join code)
4. Check webhook URL is correct in Twilio
5. Check logs: `tail -f logs/taskflow.log`

### Issue: "Cannot send messages"

**Solution:**
1. Verify Twilio credentials in `.env`
2. Check Twilio account has credit (even free tier needs activation)
3. Ensure phone number format: `whatsapp:+14155238886`
4. Check logs for specific error messages

### Issue: Port 8000 already in use

**Solution:**
```bash
# Change port
PORT=8001 python -m app.main

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Issue: Virtual environment issues

**Solution:**
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Environment mode |
| `DEBUG` | No | `False` | Debug mode (skips signature validation) |
| `HOST` | No | `0.0.0.0` | Server host |
| `PORT` | No | `8000` | Server port |
| `TWILIO_ACCOUNT_SID` | **Yes** | - | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | **Yes** | - | Twilio Auth Token |
| `TWILIO_WHATSAPP_NUMBER` | **Yes** | - | Twilio WhatsApp number |
| `GEMINI_API_KEY` | No | - | Google Gemini API key (Phase 2+) |
| `SERPAPI_KEY` | No | - | SerpAPI key (Phase 3+) |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## Next Steps

After successful setup:

1. ✅ **Test the bot** - Send messages and verify responses
2. ✅ **Review logs** - Check `logs/taskflow.log` for activity
3. ✅ **Read Phase 2 docs** - Prepare for AI integration
4. ✅ **Star the repo** - Share with others!

## Getting Help

- **Check logs:** `tail -f logs/taskflow.log`
- **Twilio Debugger:** [console.twilio.com/monitor/debugger](https://console.twilio.com/monitor/debugger)
- **Test endpoint:** `curl http://localhost:8000/health`

---

**Happy building with TaskFlow! 🚀**

