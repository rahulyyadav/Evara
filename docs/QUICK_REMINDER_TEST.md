# ⚡ Quick Reminder Test Guide

## After Deploying to Render

### Step 1: Set a Test Reminder (via WhatsApp)

Send this to your agent:
```
remind me to test at 11:30AM IST today
```

### Step 2: Check if it was stored

Visit (replace with your Render URL):
```
https://your-app-name.onrender.com/debug/reminders
```

**Expected Response:**
```json
{
  "current_time_ist": "2025-11-10 11:28:30 AM IST",
  "pending_reminders_count": 1,
  "reminders": [
    {
      "id": "abc123...",
      "task": "test",
      "user": "919876543210",
      "scheduled_time": "2025-11-10 11:30:00 AM IST",
      "time_diff_seconds": -90,
      "status": "FUTURE"
    }
  ]
}
```

✅ **Good Signs:**
- `pending_reminders_count` is 1
- `user` has your phone number
- `scheduled_time` matches what you set
- `status` is "FUTURE" (or "DUE" if at the time)

❌ **Bad Signs:**
- `pending_reminders_count` is 0 → Reminder not being stored
- `user` is null → User number issue
- `scheduled_time` is wrong → Timezone issue

### Step 3: Monitor Render Logs

1. Go to Render dashboard
2. Click your service
3. Click "Logs"
4. Search for these emojis:

**What you should see every 15 seconds:**
```
⏰ Reminder check at 11:28:45 AM IST - Found 1 pending reminder(s)
📋 Reminder abc123... for 919876543210: Due at 11:30:00 AM, Time diff: -75.0s, Status: waiting
```

**At 11:30 AM, you should see:**
```
⏰ Reminder check at 11:30:05 AM IST - Found 1 pending reminder(s)
📋 Reminder abc123... for 919876543210: Due at 11:30:00 AM, Time diff: 5.2s, Status: DUE!
🔔 FIRING REMINDER abc123... for 919876543210 - 'test'
📤 Sending reminder to WhatsApp number: +919876543210
✅ Successfully sent reminder to +919876543210: test
```

### Step 4: Check WhatsApp

You should receive a message at 11:30 AM IST:
```
⏰ REMINDER:
📝 test

Want me to snooze for 1 hour?
```

## Troubleshooting

### If reminder count is 0:

**Problem**: Reminders not being stored

**Debug:**
```bash
# Check if memory file exists on Render
# Note: Render's filesystem is ephemeral!
# Files are lost on restart/redeploy
```

**Solution**: 
- Reminders work until next deploy
- For persistence, need database (Supabase/MongoDB)
- Current implementation is for testing

### If logs show ❌ Failed to send:

**Problem**: Meta WhatsApp API issue

**Check:**
1. Meta Access Token is valid
2. Phone Number ID is correct
3. Your phone number is verified in Meta Business Suite
4. You haven't exceeded rate limits

**Fix:**
1. Go to Meta Business Suite
2. Verify your phone number status
3. Check API credentials in `.env`
4. Regenerate token if needed

### If time_diff is way off:

**Problem**: Timezone issue

**Check:**
```json
{
  "scheduled_time": "2025-11-10 11:30:00 AM IST",  // ← Should be IST
  "time_diff_seconds": 5.2,  // ← Should be small positive number when due
  "status": "DUE"  // ← Should be DUE at scheduled time
}
```

**Fix**: Already fixed in the code! But verify server time:
```bash
# Check server timezone
date
```

## Quick Command Reference

### Check reminders
```bash
curl https://your-app.onrender.com/debug/reminders
```

### Check health
```bash
curl https://your-app.onrender.com/health
```

### View logs (on Render)
1. Dashboard → Your Service → Logs
2. Search for: 🔔 or ⏰ or ❌

### Test locally
```bash
cd taskflow
# Set LOG_LEVEL=DEBUG in .env
python3 -m uvicorn app.main:app --reload --port 8000

# Then visit:
# http://localhost:8000/debug/reminders
```

## What Success Looks Like

✅ **Perfect Flow:**

1. **11:28 AM** - You set reminder
2. **11:28 AM** - Agent confirms
3. **11:28 AM** - `/debug/reminders` shows it
4. **11:28-11:30** - Logs show "waiting"
5. **11:30 AM** - Logs show "🔔 FIRING"
6. **11:30 AM** - Logs show "✅ Successfully sent"
7. **11:30 AM** - You receive WhatsApp message
8. **11:30 AM** - `/debug/reminders` shows "PAST"

## What to Share if It Doesn't Work

1. **Output of `/debug/reminders`**
2. **Logs from Render** (search for 🔔 or ⏰)
3. **Screenshot of WhatsApp conversation**
4. **Time you set the reminder** (in IST)
5. **Time it was supposed to fire** (in IST)
6. **Did you receive the message?** (yes/no)

---

**Ready to test!** Deploy and follow the steps above. 🚀

