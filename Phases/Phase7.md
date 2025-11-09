Create proper configuration management.

File: config.py

Environment Variables Needed:
1. TWILIO_ACCOUNT_SID
2. TWILIO_AUTH_TOKEN
3. TWILIO_WHATSAPP_NUMBER (sandbox: whatsapp:+14155238886)
4. GEMINI_API_KEY
5. SERPAPI_KEY
6. ENVIRONMENT (dev/prod)

Create:
1. Config class using pydantic BaseSettings
2. Load from .env file
3. Validate all required keys present
4. Provide defaults for optional settings

Also create:
- requirements.txt with all dependencies
- .env.example template
- .gitignore (ignore .env, data/, __pycache__)

requirements.txt should include:
fastapi
uvicorn[standard]
python-dotenv
google-generativeai
twilio
httpx
playwright
python-dateutil
pydantic
pydantic-settings

Add README.md with:
1. Project description
2. Setup instructions (get API keys, install deps)
3. How to run locally
4. How to test with Twilio sandbox
5. Architecture explanation
6. Future improvements