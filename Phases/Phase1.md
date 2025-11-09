Create a WhatsApp AI task automation agent called TaskFlow. This is a production-grade system, not a demo.

Tech Stack:

- Backend: Python 3.11+ with FastAPI
- AI: Google Gemini API (free tier)
- WhatsApp: Twilio WhatsApp Sandbox (free)
- Tools: SerpAPI (free tier), Playwright for web scraping
- Memory: JSON file storage for now (will scale to Supabase later)
- Deployment: Render free tier

Project Structure:
taskflow/
├── app/
│ ├── main.py # FastAPI app
│ ├── agent.py # Core agent orchestration logic
│ ├── tools/
│ │ ├── **init**.py
│ │ ├── flight_search.py # SerpAPI flight search
│ │ ├── price_tracker.py # Web scraping for prices
│ │ └── reminders.py # Reminder system
│ ├── memory/
│ │ ├── **init**.py
│ │ └── store.py # JSON-based memory
│ └── config.py # Environment variables
├── data/
│ └── user_memory.json # Persistent storage
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

Step 1: Set up the FastAPI application with Twilio WhatsApp webhook endpoint.

Requirements:

- POST /webhook endpoint to receive WhatsApp messages
- Validate Twilio signature for security
- Parse incoming message body and sender number
- Send responses back via Twilio WhatsApp API
- Async/await for all operations
- Proper error handling and logging
- Environment variables for API keys

Create main.py with:

1. FastAPI app initialization
2. Twilio webhook endpoint that receives messages
3. Function to send WhatsApp messages back to user
4. Proper request validation
5. Structured logging (user message received, agent processing, response sent)

Make sure the code is production-ready with proper error handling.
