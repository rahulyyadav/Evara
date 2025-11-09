# 🤖 Evara - WhatsApp AI Task Automation Agent

Evara is a production-grade WhatsApp AI agent that helps you automate tasks through natural conversations. Built with FastAPI, Meta WhatsApp Business API, and Google Gemini AI.

## 📋 Current Status: Phase 7 Complete ✅

**All Phases Implemented:**
- ✅ Phase 1: FastAPI + Meta WhatsApp Business API webhook
- ✅ Phase 2: AI agent orchestration with Google Gemini
- ✅ Phase 3: Flight search with SerpAPI
- ✅ Phase 4: Price tracking with Playwright
- ✅ Phase 5: Reminder system
- ✅ Phase 6: Persistent memory with thread-safe operations
- ✅ Phase 7: Configuration management

## 🚀 Tech Stack

- **Backend:** Python 3.11+ with FastAPI
- **WhatsApp:** Meta WhatsApp Business API
- **AI:** Google Gemini 1.5 Flash
- **Tools:** SerpAPI (flight search), Playwright (web scraping)
- **Storage:** JSON file storage with thread-safe operations and backups
- **Configuration:** Pydantic Settings with environment variable validation
- **Deployment:** Production-ready with Gunicorn

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Meta WhatsApp Business API credentials
- Google Gemini API key (for AI features)
- SerpAPI key (for flight search, optional)
- Playwright with Chromium (for price tracking, optional)

### Setup Steps

1. **Clone and navigate to the project:**
```bash
cd taskflow
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers (for price tracking):**
```bash
playwright install chromium
```
> **Note:** Chromium is only needed for price tracking. Other features work without it.

5. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

**Required:**
- `META_ACCESS_TOKEN`: From [Meta Developer Console](https://developers.facebook.com/)
- `PHONE_NUMBER_ID`: Your WhatsApp Business phone number ID
- `META_VERIFY_TOKEN`: Webhook verification token (use a strong random string)

**Optional (for full functionality):**
- `GEMINI_API_KEY`: From [Google AI Studio](https://makersuite.google.com/app/apikey)
- `SERPAPI_KEY`: From [SerpAPI](https://serpapi.com/) (for flight search)
- `ENVIRONMENT`: `dev` or `prod` (default: `dev`)

6. **Create necessary directories:**
```bash
mkdir -p data logs
```

## 🏃‍♂️ Running the Application

### Development Mode

```bash
# From the taskflow directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python -m app.main
```

The application will start on `http://localhost:8000`

### Production Mode

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info
```

## 🌐 Meta WhatsApp Webhook Setup

1. **Start your application** (locally or deployed)

2. **Expose your local server** (for local development):
```bash
# Using ngrok
ngrok http 8000
```

3. **Configure Meta Webhook:**
   - Go to [Meta Developer Console](https://developers.facebook.com/apps)
   - Select your app → WhatsApp → Configuration
   - Set **Webhook URL**: `https://your-url.com/webhook`
   - Set **Verify Token**: Same as your `META_VERIFY_TOKEN` env variable
   - Subscribe to `messages` field
   - Click "Verify and Save"

4. **Test the bot:**
   - Send any message to your WhatsApp Business number
   - Try: "Find flights from Delhi to Mumbai"

## 📡 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "app": "Evara",
  "version": "1.0.0",
  "status": "healthy",
  "environment": "dev"
}
```

### `GET /health`
Detailed health status
```json
{
  "status": "healthy",
  "app": "Evara",
  "version": "1.0.0",
  "environment": "dev",
  "meta_configured": true
}
```

### `POST /webhook`
Meta WhatsApp Business API webhook endpoint (receives messages from users)

### `GET /webhook`
Webhook validation endpoint

### `GET /docs`
Interactive API documentation (Swagger UI)

## 🎯 Features

### 1. Flight Search
Search for flights using natural language:
- "Find flights from Delhi to Mumbai on December 15"
- "Cheap flights to Goa tomorrow"
- "Flights from Bangalore to Chennai next Friday"

### 2. Price Tracking
Track product prices on Amazon:
- "Track iPhone 15 price on Amazon"
- "Track this product: [URL]"
- "Check my tracked items"
- "Stop tracking [product name]"

### 3. Reminders
Set and manage reminders:
- "Remind me to call doctor tomorrow at 3pm"
- "Set reminder for meeting on Dec 20 at 2pm"
- "Show my reminders"
- "Cancel reminder [ID]"

### 4. General Chat
Have natural conversations with the AI agent

## 📝 Logging

Logs are written to both:
- **Console:** Simple format for development
- **File:** `logs/evara.log` with rotation (10MB max, 5 backups)

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

Configure via `LOG_LEVEL` in `.env`

## 🔒 Security Features

- ✅ Meta webhook verification
- ✅ Environment variable configuration (no hardcoded credentials)
- ✅ Secure token handling
- ✅ Input validation with Pydantic
- ✅ Thread-safe file operations
- ✅ Atomic writes for data integrity

## 📂 Project Structure

```
taskflow/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & Meta WhatsApp webhook
│   ├── config.py            # Configuration management (Pydantic)
│   ├── agent.py             # AI agent orchestration
│   ├── tools/               # Automation tools
│   │   ├── __init__.py
│   │   ├── flight_search.py # Flight search with SerpAPI
│   │   ├── price_tracker.py # Price tracking with Playwright
│   │   └── reminder.py      # Reminder management
│   ├── memory/              # Memory management
│   │   ├── __init__.py
│   │   └── store.py         # Persistent memory with backups
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logging setup
├── data/                    # User memory storage
│   └── backups/             # Daily backups
├── logs/                    # Application logs
├── requirements.txt
├── .env.example            # Environment variable template
├── .env                    # Your actual config (gitignored)
├── .gitignore
├── README.md
└── TESTING_GUIDE.md        # Testing instructions
```

## 🧪 Testing

### Local Testing

Test the webhook locally:

```bash
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello TaskFlow" \
  -d "MessageSid=test123"
```

### Automated Testing

Run the test script:
```bash
python test_features.py
```

This will test:
- Health check
- Flight search
- Price tracking
- Reminders
- General chat

### Testing Guide

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions.

## 🚢 Deployment (Render/Heroku/VPS)

### Render Deployment

1. **Push to GitHub**

2. **Connect to Render:**
   - New Web Service
   - Connect repository
   - Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Start Command: `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add environment variables** in Render dashboard:
   - `META_ACCESS_TOKEN`
   - `PHONE_NUMBER_ID`
   - `META_VERIFY_TOKEN`
   - `GEMINI_API_KEY`
   - `SERPAPI_KEY` (optional)
   - `ENVIRONMENT=prod`

4. **Update Meta webhook** with Render URL

### Environment Variables for Production

Make sure to set all required variables in your deployment platform:
- Required: `META_ACCESS_TOKEN`, `PHONE_NUMBER_ID`, `META_VERIFY_TOKEN`
- Recommended: `GEMINI_API_KEY`, `SERPAPI_KEY`
- Optional: `ENVIRONMENT=prod`, `LOG_LEVEL=INFO`

## 🛠️ Development

### Code Style

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Configuration Management

All configuration is managed through environment variables using Pydantic Settings:

- **Required variables** are validated at startup
- **Optional variables** have sensible defaults
- **Type validation** ensures correct data types
- **Automatic .env loading** for local development

See `.env.example` for all available variables.

## 🏗️ Architecture

### Agent Orchestration Flow

1. **Message Reception**: Meta WhatsApp webhook receives WhatsApp message
2. **Intent Classification**: Gemini AI classifies user intent
3. **Tool Selection**: Agent selects appropriate tool based on intent
4. **Tool Execution**: Tool performs the requested action
5. **Response Generation**: Gemini AI generates natural language response
6. **Memory Storage**: Conversation saved to persistent memory
7. **Message Sending**: Response sent via Meta WhatsApp Business API

### Memory System

- **Thread-safe operations** with file locking
- **Atomic writes** prevent data corruption
- **Daily backups** with 7-day retention
- **Automatic migration** from old formats
- **Fast in-memory lookups** with JSON storage

### Tool System

- **Modular design**: Each tool is independent
- **Graceful degradation**: Works without optional dependencies
- **Error handling**: Robust retry logic and fallbacks
- **Caching**: Reduces API calls and improves performance

## 🔮 Future Improvements

- [ ] Database migration (Supabase/PostgreSQL)
- [ ] Multi-language support
- [ ] Voice message handling
- [ ] Image processing
- [ ] Advanced analytics
- [ ] User authentication
- [ ] Admin dashboard
- [ ] Rate limiting
- [ ] WebSocket support for real-time updates

## 📖 Documentation

- [docs/TESTING_GUIDE.md](../docs/TESTING_GUIDE.md) - How to test features
- [docs/CHROMIUM_NEEDED.md](../docs/CHROMIUM_NEEDED.md) - Playwright/Chromium requirements
- [docs/DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md) - Deployment instructions
- [docs/META_SETUP_GUIDE.md](../docs/META_SETUP_GUIDE.md) - Meta WhatsApp setup
- API Documentation: `http://localhost:8000/docs` (when running)

## 🤝 Contributing

This is a phased development project. Each phase builds upon the previous one:
- **Phase 1:** ✅ FastAPI + Meta WhatsApp Business API webhook
- **Phase 2:** ✅ AI integration with Gemini
- **Phase 3:** ✅ Flight search
- **Phase 4:** ✅ Price tracking
- **Phase 5:** ✅ Reminder system
- **Phase 6:** ✅ Persistent memory
- **Phase 7:** ✅ Configuration management

## 📄 License

MIT License

## 🆘 Troubleshooting

### Issue: Configuration Error on Startup
**Solution:** Ensure all required environment variables are set in `.env`:
- `META_ACCESS_TOKEN`
- `PHONE_NUMBER_ID`
- `META_VERIFY_TOKEN`

### Issue: Meta webhook verification fails
**Solution:** Ensure your verify token in Meta console exactly matches `META_VERIFY_TOKEN` in your environment variables

### Issue: Messages not being received
**Solution:** 
- Check Meta webhook is configured correctly
- Verify webhook URL is correct and accessible
- Ensure webhook is subscribed to `messages` field
- Check logs for errors: `tail -f logs/evara.log`

### Issue: Cannot send messages
**Solution:**
- Verify `META_ACCESS_TOKEN` is valid and not expired
- Check `PHONE_NUMBER_ID` is correct
- Ensure your phone number is added as a test number in Meta console

### Issue: Gemini API errors
**Solution:**
- Verify `GEMINI_API_KEY` is set correctly
- Check API quota and limits
- Agent will use fallback responses if Gemini is unavailable

### Issue: Playwright/Chromium errors
**Solution:**
- Run `playwright install chromium`
- Chromium is only needed for price tracking
- Other features work without it

### Issue: Memory file corruption
**Solution:**
- Check `data/backups/` for daily backups
- System automatically restores from backup if corruption detected
- Manual restore: copy backup file to `data/user_memory.json`

## 📞 Support

For issues and questions:
- Check the logs: `logs/evara.log`
- Review Meta webhook logs: https://developers.facebook.com/apps → Your App → WhatsApp → Webhooks
- Verify environment variables are set correctly
- Check API keys are valid and have quota

---

**Built with ❤️ for production use**

**Version:** 1.0.0  
**Status:** Production Ready ✅
