# 📱 Meta WhatsApp Business API Setup Guide

## Quick Setup for Your Personal Number

### Step 1: Get Your Credentials (Already Done ✅)

You already have:

- `META_ACCESS_TOKEN`
- `PHONE_NUMBER_ID`
- `WHATSAPP_BUSINESS_ID`

These are in your `.env` file.

---

### Step 2: Configure Webhook in Meta Developer Console

1. **Go to Meta Developer Console**

   - Visit: https://developers.facebook.com/apps/
   - Select your app

2. **Navigate to WhatsApp → Configuration**

   - Go to: WhatsApp → Configuration → Webhooks

3. **Add Webhook URL**

   - **Callback URL**: `https://your-render-url.onrender.com/webhook`
   - **Verify Token**: Use the same value as your `META_VERIFY_TOKEN` in `.env` file
   - Click "Verify and Save"
   
   **Security Note**: Use a strong, unique verify token. Never commit it to your code repository.

4. **Subscribe to Webhook Fields**
   - Check: `messages`
   - This allows your app to receive incoming messages

---

### Step 3: Test Your Integration

1. **Start your server** (locally or on Render)

2. **Send a test message** to your personal WhatsApp number

3. **Check logs** to see if message was received

---

## API Format (As Per Meta Documentation)

### Sending Messages

The code uses Meta's exact API format from the image:

```bash
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages
Authorization: Bearer {META_ACCESS_TOKEN}
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "text",
  "text": {
    "body": "Your message here"
  }
}
```

### Receiving Messages

Meta sends webhooks in this format:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "1234567890",
                "id": "...",
                "text": {
                  "body": "message content"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

---

## Webhook Verification

Meta requires webhook verification on first setup:

1. **GET Request** to `/webhook` with:

   - `hub.mode=subscribe`
   - `hub.verify_token=your_verify_token`
   - `hub.challenge=random_string`

2. **Your server responds** with the `hub.challenge` value

3. **Meta verifies** and subscribes to your webhook

---

## Environment Variables

Make sure your `.env` has:

```bash
# Required - Set these in your .env file
META_ACCESS_TOKEN=your_access_token
PHONE_NUMBER_ID=your_phone_number_id
META_VERIFY_TOKEN=your_strong_unique_verify_token_here

# Optional
WHATSAPP_BUSINESS_ID=your_business_id
```

**Security Best Practices:**
- Use a strong, random string for META_VERIFY_TOKEN (e.g., generate with: `openssl rand -hex 32`)
- Never commit your `.env` file to version control
- Use different verify tokens for development and production

---

## Troubleshooting

### Issue: Webhook verification fails

- Check that `META_VERIFY_TOKEN` in `.env` matches what you entered in Meta console
- Ensure webhook URL is accessible (not localhost)

### Issue: Messages not received

- Check Meta webhook logs: https://developers.facebook.com/apps/ → Your App → WhatsApp → Webhooks
- Verify webhook is subscribed to `messages` field
- Check your server logs for incoming requests

### Issue: Can't send messages

- Verify `META_ACCESS_TOKEN` is valid and not expired
- Check `PHONE_NUMBER_ID` is correct
- Ensure your phone number is added as a test number in Meta console

---

## Code Integration

The integration is complete! The code:

- ✅ Uses Meta's exact API format from documentation
- ✅ Handles webhook verification automatically
- ✅ Parses incoming messages correctly
- ✅ Sends messages using the correct format
- ✅ Works with your personal number

Just deploy to Render and configure the webhook! 🚀
