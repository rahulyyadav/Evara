Implement a simple but functional reminder system.

File: tools/reminders.py

This tool should:

1. Parse reminder requests using Gemini
2. Extract: task description, datetime
3. Store in memory
4. Check every minute for due reminders
5. Send WhatsApp message when time comes

Supported Formats:

- "Remind me to call doctor tomorrow at 3pm"
- "Set reminder for electricity bill on 10th December"
- "Remind me to take medicine in 2 hours"
- "Show my reminders"
- "Cancel reminder [number]"

Key Requirements:

- Parse relative times ("tomorrow", "in 2 hours", "next Monday")
- Parse absolute times ("10th December at 3pm")
- Store in IST timezone
- Background job to check reminders (simple loop for v1)
- Mark as "sent" after sending

Features:

1. Create reminder
2. List all reminders
3. Cancel reminder
4. Snooze reminder (optional for v1)

Response Format (Creating):
"✅ Reminder set!
📅 Dec 10, 2025 at 3:00 PM
📝 Call doctor

You have 3 active reminders."

Response Format (When Due):
"⏰ REMINDER:
📝 Call doctor

Want me to snooze for 1 hour?"

Memory Structure:
{
"user_number": {
"reminders": [
{
"id": "uuid",
"task": "Call doctor",
"datetime": "2025-12-10T15:00:00",
"status": "pending", // or "sent", "cancelled"
"created_at": "2025-11-06T10:30:00"
}
]
}
}

Implement with:

1. ReminderTool class
2. create_reminder() async method
3. list_reminders()
4. cancel_reminder()
5. check_due_reminders() - background job
6. \_parse_datetime() using Gemini or dateparser library
7. \_send_reminder_notification() via Twilio
