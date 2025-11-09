Implement persistent memory system using JSON file storage.

File: memory/store.py

This memory should:

1. Store user conversations and context
2. Store tool-specific data (tracked products, reminders)
3. Store user preferences
4. Load on agent startup
5. Save after every interaction
6. Handle concurrent access safely

Memory Structure:
{
"users": {
"whatsapp:+919876543210": {
"first_seen": "2025-11-06T10:00:00",
"last_interaction": "2025-11-06T16:30:00",
"preferences": {
"default_origin": "Delhi",
"preferred_airlines": ["IndiGo"],
"price_alert_threshold": 5 // percent
},
"conversation_history": [
{
"timestamp": "2025-11-06T16:30:00",
"user_message": "Find flights to Mumbai",
"agent_response": "...",
"intent": "flight_search",
"tool_used": "flight_search"
}
],
"tracked_products": [...],
"reminders": [...]
}
}
}

Key Requirements:

- Thread-safe file operations (use file locking)
- Atomic writes (write to temp file, then rename)
- Keep only last 50 conversations per user (memory optimization)
- Backup system (daily backup of user_memory.json)
- Fast lookups (load entire file into memory at startup)

Implement with:

1. MemoryStore class (singleton)
2. load() - Read from JSON file
3. save() - Write to JSON file atomically
4. get_user_context(phone_number)
5. save_conversation(phone_number, message, response, intent)
6. get_tracked_products(phone_number)
7. get_reminders(phone_number)
8. update_preferences(phone_number, prefs)

Add proper error handling for corrupted JSON, disk full, etc.
