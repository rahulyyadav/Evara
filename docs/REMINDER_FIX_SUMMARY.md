# 🔧 Reminder System Fix - Debugging & Improvements

## Problem Reported

❌ **Issue**: Reminders are being SET (agent confirms), but NOT being SENT at the scheduled time.

**Example from User:**
- User sets reminder at 11:02 AM IST for 11:05 AM IST  
- Agent confirms: "Okay, I will remind you to send your wife the 'iloyouu budhi' message at 11:05 AM IST today!"
- ❌ At 11:05 AM, no reminder is sent

## Root Cause Analysis

### Investigation Steps:

1. ✅ **Reminder Storage** - Working correctly
   - Reminders are being stored in memory
   - `add_reminder()` function is working
   - User number is added by `get_all_pending_reminders()`

2. ✅ **Timezone Handling** - Fixed
   - Reminders store timezone information
   - Comparison converts to IST correctly

3. ⚠️  **Logging** - Was insufficient
   - No visibility into reminder checker execution
   - Couldn't see if reminders were being found
   - No debugging info for time comparisons

4. ⚠️  **User Number Format** - Potential issue
   - Meta WhatsApp requires "+" prefix
   - Wasn't being added consistently

## Changes Implemented

### 1. Enhanced Logging 📊

**Added detailed logging to `check_reminders_loop`:**

```python
# Every check cycle
logger.debug(f"⏰ Reminder check at {now_ist.strftime('%I:%M:%S %p IST')} - Found {len(pending_reminders)} pending reminder(s)")

# For each reminder
logger.debug(f"📋 Reminder {reminder_id[:8]}... for {user_number}: "
           f"Due at {reminder_dt.strftime('%I:%M:%S %p')}, "
           f"Time diff: {time_diff:.1f}s, "
           f"Status: {'DUE!' if 0 <= time_diff < 20 else 'waiting'}")

# When firing
logger.info(f"🔔 FIRING REMINDER {reminder_id[:8]}... for {user_number} - '{task}'")
logger.info(f"📤 Sending reminder to WhatsApp number: {whatsapp_number}")

# After sending
logger.info(f"✅ Successfully sent reminder to {whatsapp_number}: {task}")
# OR
logger.error(f"❌ Failed to send reminder to {whatsapp_number} - send_whatsapp_message returned False")
```

### 2. Fixed User Number Format 🔧

**Ensures "+" prefix for Meta WhatsApp:**

```python
# Format user number for WhatsApp
# Meta format: Need to ensure it has + prefix
if not user_number.startswith("+"):
    whatsapp_number = f"+{user_number}"
else:
    whatsapp_number = user_number
```

### 3. Added Debug Endpoint 🛠️

**New endpoint to inspect reminders in real-time:**

```bash
GET /debug/reminders
```

**Returns:**
```json
{
  "current_time_ist": "2025-11-10 11:05:30 PM IST",
  "pending_reminders_count": 2,
  "reminders": [
    {
      "id": "abc123...",
      "task": "send my wife 'iloyouu budhi' message",
      "user": "1234567890",
      "scheduled_time": "2025-11-10 11:05:00 AM IST",
      "time_diff_seconds": 30.5,
      "status": "DUE"
    }
  ]
}
```

### 4. Improved Error Handling ⚠️

**Better error messages and exception handling:**

```python
if not reminder_dt_str:
    logger.warning(f"⚠️  Reminder {reminder_id} missing datetime field")
    continue

if not user_number:
    logger.warning(f"⚠️  Reminder {reminder_id} missing user_number field")
    continue
```

## How to Debug

### Step 1: Check if Reminder is Stored

Visit the debug endpoint after setting a reminder:
```bash
https://your-app.onrender.com/debug/reminders
```

**What to look for:**
- ✅ `pending_reminders_count` > 0
- ✅ Your reminder appears in the list
- ✅ `scheduled_time` is correct
- ✅ `user` field has a phone number
- ✅ `status` shows "FUTURE" (before time) or "DUE" (at time)

### Step 2: Check Logs on Render

1. Go to Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Search for emoji indicators:

**What to look for:**
```
🔄 Reminder checker loop started
⏰ Reminder check at 11:05:15 AM IST - Found 1 pending reminder(s)
📋 Reminder abc123... for 1234567890: Due at 11:05:00 AM, Time diff: 15.2s, Status: DUE!
🔔 FIRING REMINDER abc123... for 1234567890 - 'send my wife iloyouu budhi message'
📤 Sending reminder to WhatsApp number: +1234567890
✅ Successfully sent reminder to +1234567890: send my wife iloyouu budhi message
```

**If you see ❌ errors:**
```
❌ Failed to send reminder to +1234567890 - send_whatsapp_message returned False
→ Check Meta WhatsApp API credentials
→ Check phone number format
→ Check Meta API rate limits
```

### Step 3: Local Testing

Test locally first to isolate the problem:

```bash
cd taskflow

# Set reminder for 1 minute from now
python -c "
from app.tools.reminder import ReminderTool
from app.memory import MemoryStore
import asyncio

async def test():
    tool = ReminderTool(MemoryStore())
    result = await tool.set_reminder(
        '+1234567890',
        'Test reminder',
        'in 1 minute'
    )
    print(result)

asyncio.run(test())
"

# Then check if it appears
curl http://localhost:8000/debug/reminders
```

## Possible Issues & Solutions

### Issue 1: Reminders Not Being Stored

**Symptoms:**
- Agent confirms but `/debug/reminders` shows 0 reminders
- `pending_reminders_count` is 0

**Solutions:**
1. Check if memory file is being saved correctly
2. Check file permissions on Render
3. Check if memory store is persisting (Render's ephemeral filesystem)

**Fix for Render's Ephemeral Filesystem:**
```bash
# On Render, the filesystem resets on deploy
# You need to use a persistent volume or external database
# For now, reminders only persist until next deploy
```

### Issue 2: Reminders Not Being Sent

**Symptoms:**
- `/debug/reminders` shows reminders with status "DUE"
- Logs show "🔔 FIRING REMINDER"
- But no WhatsApp message received

**Solutions:**
1. **Check Meta WhatsApp API status:**
   - Go to Meta Business Suite
   - Check if phone number is verified
   - Check if API token is valid

2. **Check phone number format:**
   - Must include country code
   - Must start with "+"
   - Example: +919876543210 (India)

3. **Check rate limits:**
   - Meta has messaging limits
   - Check if you've exceeded daily limit

### Issue 3: Wrong Timezone

**Symptoms:**
- Reminder fires at wrong time
- Time diff shows large negative or positive values

**Solutions:**
1. **Check reminder storage timezone:**
   ```python
   # Should store with timezone info
   "datetime": "2025-11-10T11:05:00+05:30"  # IST
   ```

2. **Check server timezone:**
   ```bash
   # On Render, check what timezone the server is in
   date
   # Should show IST or you need to convert
   ```

### Issue 4: Reminder Checker Not Running

**Symptoms:**
- No logs from reminder checker
- No "🔄 Reminder checker loop started" in logs

**Solutions:**
1. **Check if background task started:**
   ```bash
   # Look for startup logs
   grep "Reminder checker started" logs/evara.log
   ```

2. **Restart the service:**
   - On Render: Manual Deploy → Clear build cache & deploy

## Testing Checklist

Before deploying, test locally:

- [ ] Set reminder for 1 minute from now
- [ ] Check `/debug/reminders` endpoint
- [ ] Wait for 1 minute
- [ ] Check logs for "🔔 FIRING REMINDER"
- [ ] Verify WhatsApp message received
- [ ] Check reminder marked as "sent" in memory

On Render (after deploy):

- [ ] Check health endpoint: `/health`
- [ ] Set test reminder via WhatsApp
- [ ] Check `/debug/reminders` endpoint
- [ ] Monitor logs in Render dashboard
- [ ] Verify reminder fires at correct time
- [ ] Check timezone is correct (IST)

## Next Steps

1. **Deploy to Render** ✅
   ```bash
   git add -A
   git commit -m "Fix: Enhanced reminder logging and debugging"
   git push origin main
   ```

2. **Test on Production** 🧪
   - Set a reminder for 2-3 minutes from now
   - Check `/debug/reminders`
   - Monitor Render logs
   - Wait for reminder to fire

3. **Monitor Logs** 📊
   - Watch for the emoji indicators
   - Check for any ❌ errors
   - Verify timezone is correct

4. **If Still Not Working** 🔍
   - Share the `/debug/reminders` output
   - Share the logs from Render
   - We'll debug together

## Summary

✅ **Completed:**
- Added comprehensive logging
- Fixed user number format for Meta
- Added debug endpoint
- Improved error handling
- Fixed timezone comparison

🚀 **Ready to Deploy:**
- All changes are backward compatible
- No breaking changes
- Enhanced debugging capabilities

📝 **To Test:**
- Deploy to Render
- Set a test reminder
- Check logs and debug endpoint
- Verify it fires correctly

---

**Note**: If reminders still don't work after this, it's likely one of:
1. Render's ephemeral filesystem (reminders lost on restart)
2. Meta WhatsApp API credentials/permissions
3. Phone number format/verification issue

We'll debug further based on the logs and debug endpoint output! 🔍

