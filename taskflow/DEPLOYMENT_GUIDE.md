# 🚀 TaskFlow Deployment Guide

## Quick Setup (1-2 hours total)

### Step 1: Get WhatsApp Number (10-15 minutes) ⭐ DO THIS FIRST

#### Option A: Twilio WhatsApp Sandbox (FREE - Recommended)

1. **Sign up for Twilio** (Free Trial)

   - Go to: https://www.twilio.com/try-twilio
   - Sign up with email/phone
   - Verify your email and phone number
   - You'll get $15.50 free credit (enough for testing)

2. **Enable WhatsApp Sandbox**

   - Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
   - You'll see a sandbox number: `whatsapp:+14155238886`
   - Note your **Join Code** (e.g., "join example-code")

3. **Join the Sandbox**

   - Open WhatsApp on your phone
   - Send the join code to: `+1 415 523 8886`
   - Example: Send "join example-code" to that number
   - You'll get a confirmation message

4. **Get Your Credentials**
   - Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
   - Note down:
     - **Account SID** (starts with AC...)
     - **Auth Token** (click to reveal)
     - **WhatsApp Number**: `whatsapp:+14155238886`

✅ **You now have a FREE WhatsApp number!**

---

### Step 2: Deploy to Render (20-30 minutes)

#### Prerequisites

- GitHub account
- Code pushed to GitHub repository

#### Deployment Steps

1. **Push Code to GitHub**

   ```bash
   cd taskflow
   git init
   git add .
   git commit -m "Initial commit - TaskFlow WhatsApp Agent"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create Render Account**

   - Go to: https://render.com
   - Sign up with GitHub (free)

3. **Create New Web Service**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

4. **Configure Service**

   - **Name**: `taskflow-agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. **Add Environment Variables**
   Click "Environment" tab and add:

   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   GEMINI_API_KEY=your_gemini_key (optional)
   SERPAPI_KEY=your_serpapi_key (optional)
   ENVIRONMENT=prod
   LOG_LEVEL=INFO
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your app will be live at: `https://taskflow-agent.onrender.com`

---

### Step 3: Connect WhatsApp to Render (5 minutes)

1. **Get Your Render URL**

   - After deployment, copy your Render URL
   - Example: `https://taskflow-agent.onrender.com`

2. **Configure Twilio Webhook**

   - Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
   - Find "WHEN A MESSAGE COMES IN"
   - Set URL: `https://taskflow-agent.onrender.com/webhook`
   - Method: `HTTP POST`
   - Click "Save"

3. **Test It!**
   - Send a message to: `+1 415 523 8886`
   - You should get a response!

---

## Alternative: Facebook Business API (NOT RECOMMENDED for quick setup)

❌ **Why NOT Facebook Business API:**

- Requires business verification (takes days/weeks)
- Needs business documents
- More complex setup
- Not suitable for 1-2 hour timeline
- Better for production businesses

✅ **Twilio Sandbox is perfect for:**

- Portfolio projects
- Resume projects
- Testing and development
- Quick setup (minutes, not days)

---

## Cost Comparison

| Option                | Cost       | Setup Time    | Best For                |
| --------------------- | ---------- | ------------- | ----------------------- |
| **Twilio Sandbox**    | **FREE**   | **10-15 min** | **Portfolio/Resume** ⭐ |
| Twilio Production     | $0.005/msg | 30 min        | Production apps         |
| Facebook Business     | Free       | Days/Weeks    | Businesses              |
| WhatsApp Business App | Free       | 1 hour        | Small businesses        |

---

## Troubleshooting

### Issue: Twilio webhook not receiving messages

- Check Render logs: `https://dashboard.render.com` → Your service → Logs
- Verify webhook URL is correct (no trailing slash)
- Ensure webhook is set to `HTTP POST`

### Issue: Render build fails

- Check build logs for errors
- Ensure all dependencies are in `requirements.txt`
- Verify Python version matches `runtime.txt`

### Issue: App crashes on Render

- Check memory usage (free tier has 512MB limit)
- Review logs for errors
- Ensure all environment variables are set

---

## Next Steps After Deployment

1. ✅ Test all features (flight search, price tracking, reminders)
2. ✅ Update your resume with the live project URL
3. ✅ Create a demo video showing the WhatsApp bot in action
4. ✅ Add project to your portfolio

---

## Support

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- Render Docs: https://render.com/docs
- Project Issues: Check logs in Render dashboard

---

**🎉 You're all set! Your WhatsApp AI agent is live!**
