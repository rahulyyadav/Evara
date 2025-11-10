# 🧹 Automatic Memory Cleanup - 24 Hour Auto-Delete

## What Was Implemented

✅ **Automatic cleanup of conversations older than 24 hours**
✅ **Runs every 24 hours automatically**
✅ **Keeps reminders, tracked products, and preferences intact**
✅ **Works for all users**
✅ **No impact on functionality**

## How It Works

### Background Task

A background task runs continuously that:
1. **Waits 24 hours** after app starts
2. **Scans all users** and their conversations
3. **Deletes conversations** older than 24 hours
4. **Keeps important data**:
   - ✅ Reminders (all - pending and sent)
   - ✅ Tracked products
   - ✅ User preferences
   - ✅ First seen / last interaction timestamps
5. **Saves changes** to disk
6. **Repeats** every 24 hours

### What Gets Deleted

❌ **Deleted (after 24 hours):**
- Conversation history older than 24 hours
- User messages
- Agent responses
- Intent classifications
- Tool usage logs

✅ **Kept Forever:**
- Reminders (pending and completed)
- Tracked products and price alerts
- User preferences
- User metadata (first seen, last interaction)

## Example

### Before Cleanup (Day 1 - 11:00 PM):
```json
{
  "users": {
    "919876543210": {
      "conversation_history": [
        {
          "timestamp": "2025-11-09T10:00:00",  // 37 hours ago
          "user_message": "what is the time?",
          "agent_response": "..."
        },
        {
          "timestamp": "2025-11-10T10:00:00",  // 13 hours ago
          "user_message": "search flights",
          "agent_response": "..."
        },
        {
          "timestamp": "2025-11-10T22:00:00",  // 1 hour ago
          "user_message": "track iPhone price",
          "agent_response": "..."
        }
      ],
      "reminders": [...],  // Kept
      "tracked_products": [...]  // Kept
    }
  }
}
```

### After Cleanup (Day 2 - 11:00 PM):
```json
{
  "users": {
    "919876543210": {
      "conversation_history": [
        {
          "timestamp": "2025-11-10T22:00:00",  // Within 24 hours - KEPT
          "user_message": "track iPhone price",
          "agent_response": "..."
        }
      ],
      "reminders": [...],  // Still here!
      "tracked_products": [...]  // Still here!
    }
  }
}
```

## Logs

When cleanup runs, you'll see:

```bash
# Every 24 hours
🧹 Starting scheduled memory cleanup...
✅ Cleanup complete: Deleted 45 conversations from 3 user(s). Cutoff: 2025-11-10T11:00:00

# Or if nothing to delete
✅ Cleanup complete: No old conversations to delete
```

## Why 24 Hours?

1. **Space Management**: Prevents memory file from growing indefinitely
2. **Privacy**: Doesn't keep user conversations forever
3. **Performance**: Smaller files load faster
4. **Balance**: 24 hours is enough context for multi-turn conversations

## Memory vs Context

### Short-term Context (24 hours):
- Used for **multi-turn conversations**
- Example: "search flight on 2nd dec" → "chennai to bagdogra"
- Agent remembers the date from previous turn
- **Deleted after 24 hours**

### Long-term Memory (Forever):
- **Reminders**: So they fire even after conversation is deleted
- **Tracked products**: So price alerts continue working
- **Preferences**: So agent remembers your settings
- **NOT deleted**

## Testing

### Manual Cleanup (for testing):

You can manually trigger cleanup by calling the function:

```python
# In Python console or test script
from app.memory import MemoryStore

memory = MemoryStore()
result = memory.cleanup_old_conversations(hours=24)
print(result)
# Output: {'deleted_conversations': 5, 'users_cleaned': 2, 'cutoff_time': '...'}
```

### Check Current Conversations:

```bash
# View memory file
cat data/user_memory.json | jq '.users'

# Count conversations per user
cat data/user_memory.json | jq '.users | to_entries[] | {user: .key, count: (.value.conversation_history | length)}'
```

## Configuration

**Current setting**: 24 hours (hardcoded)

**To change** (if needed):

In `app/memory/store.py`:
```python
def cleanup_old_conversations(self, hours: int = 24):  # Change this number
```

And in `app/main.py`:
```python
result = memory_store.cleanup_old_conversations(hours=24)  # Change this number
```

**Suggested values:**
- `hours=12` - More aggressive (12 hours)
- `hours=24` - Current (1 day) ✅ Recommended
- `hours=48` - Lenient (2 days)
- `hours=168` - Very lenient (1 week)

## Impact on Space

### Example Calculation:

**Average conversation:**
- ~500 characters per turn (user + agent messages)
- ~50 conversations per day per user
- = 25 KB per user per day

**With 100 users:**
- Without cleanup: ~2.5 MB per day → 75 MB per month
- With 24h cleanup: ~2.5 MB total (stays constant)

**Savings**: 97% less disk space! 🎉

## Q&A

### Q: Will this affect the agent's ability to remember context?

**A**: No! The agent uses the **last 10 messages** for context. Those are always within 24 hours for active conversations.

### Q: What happens to reminders set 2 days ago?

**A**: Reminders are **NOT deleted**. They stay in memory forever until they fire or are cancelled.

### Q: What if I set a reminder, then don't chat for 3 days?

**A**: The reminder will still fire! Conversations are deleted, but reminders remain.

### Q: Does this run on Render?

**A**: Yes! The background task runs automatically on Render. Check logs for "🧹" emoji.

### Q: What if Render restarts the app?

**A**: The cleanup task restarts automatically. It waits 24 hours before first cleanup.

### Q: Can I disable this?

**A**: Yes, comment out these lines in `app/main.py`:
```python
# _memory_cleanup_task = asyncio.create_task(cleanup_old_memory_loop(memory_store))
# logger.info("✅ Memory cleanup scheduler started")
```

## Summary

✅ **Implemented**: Auto-cleanup of conversations >24 hours old
✅ **Frequency**: Runs every 24 hours automatically
✅ **Safety**: Keeps reminders, products, preferences
✅ **Space savings**: 97% less disk usage
✅ **No impact**: Agent context and functionality unchanged
✅ **Production ready**: Tested and error-handled

**Result**: Your memory stays lean and clean, automatically! 🧹✨

