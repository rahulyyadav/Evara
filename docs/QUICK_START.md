# ⚡ Quick Start - Get WhatsApp Number in 15 Minutes

## 🎯 Goal: Get FREE WhatsApp number for your resume project

## Step-by-Step (10-15 minutes)

### 1. Sign up for Twilio (2 minutes)
- Go to: https://www.twilio.com/try-twilio
- Click "Start Free Trial"
- Enter email, password, phone number
- Verify email and phone

### 2. Enable WhatsApp Sandbox (3 minutes)
- After login, go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
- You'll see: "Join Code" and Sandbox Number
- **Sandbox Number**: `+1 415 523 8886` (this is your WhatsApp number!)
- **Join Code**: Something like "join example-123"

### 3. Join the Sandbox (2 minutes)
- Open WhatsApp on your phone
- Send the join code to: `+1 415 523 8886`
- Example: If code is "join example-123", send exactly that message
- You'll get confirmation: "You're all set! You can start sending messages..."

### 4. Get Your Credentials (3 minutes)
- Go to: https://console.twilio.com/us1/account/settings/credentials
- Copy:
  - **Account SID** (starts with AC...)
  - **Auth Token** (click eye icon to reveal)
- Go back to WhatsApp Sandbox page
- Note: **WhatsApp Number** = `whatsapp:+14155238886`

### 5. Save Credentials (1 minute)
Create `.env` file in `taskflow/` directory:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
ENVIRONMENT=dev
```

✅ **DONE! You have a FREE WhatsApp number!**

---

## 🚀 Next: Deploy to Render (20 minutes)

See `DEPLOYMENT_GUIDE.md` for full deployment instructions.

---

## 💡 Why Twilio Sandbox?

✅ **FREE** - No credit card needed for sandbox
✅ **Fast** - Setup in 10-15 minutes
✅ **Perfect for Portfolio** - Shows you can integrate APIs
✅ **Real WhatsApp** - Works with actual WhatsApp
✅ **No Business Verification** - Unlike Facebook Business API

---

## 📝 For Your Resume

You can say:
- "Built WhatsApp AI agent using Twilio API"
- "Deployed on Render cloud platform"
- "Integrated with Google Gemini AI"
- "Live project: [your-render-url]"

---

**Need help? Check `DEPLOYMENT_GUIDE.md` for detailed steps.**
