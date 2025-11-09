# 🚀 Evara Deployment Guide

## Quick Setup Guide

### Step 1: Set Up Meta WhatsApp Business API ⭐ DO THIS FIRST

Evara uses Meta WhatsApp Business API (formerly Facebook WhatsApp Business API) for WhatsApp integration.

**Prerequisites:**

- Facebook Business Account
- WhatsApp Business Account (or test number)

**Setup Steps:**

1. **Create Facebook App**

   - Go to: https://developers.facebook.com/
   - Create a new app → Select "Business" type
   - Add "WhatsApp" product to your app

2. **Get Your Credentials**

   - **Access Token**: From your app's WhatsApp settings
   - **Phone Number ID**: Your WhatsApp Business phone number ID
   - **Verify Token**: Create a strong, unique token (e.g., use a random string generator)
   - **Business Account ID**: (Optional) Your WhatsApp Business Account ID

3. **Configure Webhook**
   - Set webhook URL: `https://your-app.onrender.com/webhook`
   - Verify Token: Use the same token you set in META_VERIFY_TOKEN env variable
   - Subscribe to `messages` events

📖 **Detailed Setup**: See `META_SETUP_GUIDE.md` for complete instructions.

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
   git commit -m "Initial commit - Evara WhatsApp Agent"
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

   - **Name**: `evara-agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. **Add Environment Variables**
   Click "Environment" tab and add:

   **Required:**

   ```
   META_ACCESS_TOKEN=your_meta_access_token_here
   PHONE_NUMBER_ID=your_phone_number_id_here
   META_VERIFY_TOKEN=your_strong_verify_token_here
   ENVIRONMENT=prod
   LOG_LEVEL=INFO
   ```

   **Optional:**

   ```
   WHATSAPP_BUSINESS_ID=your_business_id (optional)
   GEMINI_API_KEY=your_gemini_key (for AI features)
   SERPAPI_KEY=your_serpapi_key (for flight search)
   ```

   **Security Note**: Generate a strong verify token using: `openssl rand -hex 32` or any secure random string generator.

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your app will be live at: `https://evara-agent.onrender.com`

---

### Step 3: Configure Meta Webhook (5 minutes)

1. **Get Your Render URL**

   - After deployment, copy your Render URL
   - Example: `https://evara-agent.onrender.com`

2. **Configure Meta Webhook**

   - Go to: https://developers.facebook.com/apps
   - Select your app → WhatsApp → Configuration
   - Set **Webhook URL**: `https://evara-agent.onrender.com/webhook`
   - Set **Verify Token**: Use the same value as your META_VERIFY_TOKEN environment variable
   - Click "Verify and Save"
   - Subscribe to `messages` field

   **Important**: The verify token in Meta console must exactly match the META_VERIFY_TOKEN in your environment variables.

3. **Test It!**
   - Send a message to your WhatsApp Business number
   - You should get a response!

---

## Meta WhatsApp Business API

✅ **Why Meta WhatsApp Business API:**

- Direct integration with WhatsApp
- No middleman (Twilio) required
- Free for development and testing
- Production-ready for businesses
- Full WhatsApp Business API features

📖 **For detailed setup instructions**, see `META_SETUP_GUIDE.md`

---

## Troubleshooting

### Issue: Meta webhook not receiving messages

- Check Render logs: `https://dashboard.render.com` → Your service → Logs
- Verify webhook URL is correct (no trailing slash)
- Ensure verify token matches in Meta dashboard and environment variable
- Check that webhook is subscribed to `messages` events
- Verify META_ACCESS_TOKEN and PHONE_NUMBER_ID are set correctly

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
