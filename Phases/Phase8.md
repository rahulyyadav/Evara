Add production-ready features:

1. Health Check Endpoint:

   - GET /health returns {"status": "healthy", "timestamp": "..."}
   - Check memory file accessible
   - Check API keys configured

2. Logging:

   - Use Python logging module
   - Log levels: INFO, WARNING, ERROR
   - Log format: timestamp, level, message
   - Log to both console and file (logs/taskflow.log)

3. Error Messages:

   - Friendly error messages for users
   - Technical errors logged but not shown
   - Example: API error → "Oops, something went wrong. Try again?"

4. Rate Limiting:

   - Prevent spam (max 10 messages per minute per user)
   - Store in memory with timestamps
   - Response: "Too many messages! Wait a minute."

5. Welcome Message:
   - First-time users get introduction
   - Explain capabilities
   - Example commands

Welcome Message:
"👋 Hey! I'm TaskFlow, your AI assistant.

I can help you with:
✈️ Search flights
💰 Track product prices
⏰ Set reminders
❓ Ask me anything!

Try: 'Find flights to Mumbai next Friday'"

6. Help Command:
   - User sends "help" → show capabilities
   - Include example commands

Add all of this to main.py and agent.py with proper structure.
