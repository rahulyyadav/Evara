# 🔍 Debugging Reminders - Not Firing

## Status

✅ **Memory**: Working perfectly  
✅ **Reminder Storage**: Reminders are being saved  
✅ **Reminder Retrieval**: Agent can see reminders  
❌ **Reminder Firing**: Reminders are NOT being sent at due time

## Test Case from WhatsApp

- **12:02 PM**: Set reminder for 12:04 PM (topic: "testing")
- **12:04 PM**: Should have received reminder ❌
- **12:07 PM**: Still no reminder (3 minutes late)
- **Result**: Reminder checker is NOT working

## Possible Causes

### 1. Background Task Not Started

**Problem**: Reminder checker loop might not be running

**Check Render Logs for:**

```bash
✅ Reminder checker started
🔄 Reminder checker loop started (checking every 15 seconds)
```

**If you DON'T see this** → Background task didn't start

---

### 2. No Pending Reminders Found

**Problem**: `get_all_pending_reminders()` returns empty

**Check Render Logs for:**

```bash
⏰ Reminder check at 12:04:15 PM IST - Found 0 pending reminder(s)
```

**If you see "Found 0"** → Reminders aren't being retrieved

---

### 3. Timezone Issue

**Problem**: Reminder time doesn't match current time

**Check `/debug/reminders` for:**

```json
{
  "time_diff_seconds": -180 // Negative = future, Positive = past
}
```

**If large negative number** → Timezone mismatch

---

### 4. Reminder Sends But Fails

**Problem**: WhatsApp API failing

**Check Render Logs for:**

```bash
🔔 FIRING REMINDER abc123...
📤 Sending reminder to WhatsApp number: +919876543210
❌ Failed to send reminder - send_whatsapp_message returned False
```

**If you see ❌** → Meta API issue

---

## Debugging Steps

### Step 1: Check Render Logs

1. Go to https://dashboard.render.com
2. Click your service
3. Click **"Logs"** tab
4. Search for these keywords (one at a time):
   - `Reminder checker started`
   - `🔄`
   - `⏰`
   - `🔔`
   - `pending reminder`

### Step 2: Check Debug Endpoint

Visit: `https://your-app.onrender.com/debug/reminders`

**Expected response:**

```json
{
  "current_time_ist": "2025-11-10 12:10:00 PM IST",
  "pending_reminders_count": 1,
  "reminders": [
    {
      "id": "abc123...",
      "task": "testing",
      "user": "919876543210",
      "scheduled_time": "2025-11-10 12:04:00 PM IST",
      "time_diff_seconds": 360,
      "status": "PAST"
    }
  ]
}
```

**What to look for:**

- ✅ `pending_reminders_count > 0` → Reminders exist
- ✅ `user` field has phone number → User number is attached
- ✅ `time_diff_seconds > 0` → Reminder is past due
- ✅ `status: "PAST"` → Should have fired

---

## Common Issues & Fixes

### Issue 1: "Found 0 pending reminders"

**Cause**: Render's ephemeral filesystem lost the memory file

**Solution**: Reminders are lost on every deploy. For production, need database.

**Temporary workaround**: Don't redeploy while waiting for reminders

---

### Issue 2: Background task not started

**Symptoms in logs**:

```
✅ Evara is ready to receive messages
```

But NO:

```
✅ Reminder checker started
```

**Fix**: Check startup code in `main.py`

**Quick fix**: Restart service on Render

---

### Issue 3: Logs say "DUE!" but nothing happens

**Symptoms**:

```
📋 Reminder abc123... Status: DUE!
```

But NO:

```
🔔 FIRING REMINDER
```

**Cause**: Time window logic issue

**Check**: Is `0 <= time_diff < 20` condition correct?

---

### Issue 4: Meta WhatsApp API failing

**Symptoms**:

```
🔔 FIRING REMINDER
📤 Sending reminder
❌ Failed to send - send_whatsapp_message returned False
```

**Causes**:

1. Meta Access Token expired
2. Phone number not verified
3. Rate limit exceeded

**Fix**: Check Meta Business Suite

---

## What to Share for Debugging

Please provide:

1. **Output of `/debug/reminders`**

   ```bash
   curl https://your-app.onrender.com/debug/reminders
   ```

2. **Last 100 lines of Render logs**

   - Filter by searching: `reminder` or `🔔` or `⏰`

3. **Environment variables** (redacted):

   - Is `META_ACCESS_TOKEN` set?
   - Is `PHONE_NUMBER_ID` set?

4. **Timeline**:
   - When was reminder set?
   - When was it supposed to fire?
   - Current time when checking

---

## Testing Locally

To test the reminder system locally:

```bash
cd taskflow

# Start the app
python3 -m uvicorn app.main:app --reload --port 8000

# In logs, look for:
# ✅ Reminder checker started
# 🔄 Reminder checker loop started

# Set a reminder via API
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "1234567890",
            "text": {"body": "remind me to test in 1 minute"}
          }]
        }
      }]
    }]
  }'

# Check debug endpoint
curl http://localhost:8000/debug/reminders

# Wait 1 minute and check logs for:
# 🔔 FIRING REMINDER
```

---

## Quick Fixes to Try

### Fix 1: Enable DEBUG logging

In `.env`:

```bash
LOG_LEVEL=DEBUG
```

Redeploy and check logs for detailed output.

---

### Fix 2: Increase check frequency

If reminders are being missed, change check interval:

In `main.py` line 97:

```python
await asyncio.sleep(15)  # Try 5 seconds instead
```

---

### Fix 3: Widen the trigger window

In `main.py` line 141:

```python
if 0 <= time_diff < 20:  # Try 60 seconds instead
```

---

## Next Steps

1. **Check Render logs** - Look for startup messages
2. **Check `/debug/reminders`** - See if reminders exist
3. **Share findings** - I'll help debug further based on what you see

The code looks correct, so it's likely an environment or timing issue on Render.
