Prepare for Render deployment:

1. Create render.yaml:
   services:

- type: web
  name: taskflow-agent
  env: python
  buildCommand: pip install -r requirements.txt && playwright install chromium
  startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  envVars:
  - key: PYTHON_VERSION
    value: 3.11.0

2. Add Procfile (backup):
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

3. Add runtime.txt:
   python-3.11.0

4. Update main.py to:

   - Use PORT from environment variable
   - Handle Render's health checks
   - Set proper CORS if needed

5. Add startup optimization:

   - Preload Playwright browser
   - Cache Gemini client
   - Load memory at startup

6. Add graceful shutdown:
   - Save memory before exit
   - Close API connections
   - Log shutdown

Make sure the app can:

- Start in under 60 seconds (Render requirement)
- Handle Render's health checks on /
- Work with Render's free tier (512MB RAM)
