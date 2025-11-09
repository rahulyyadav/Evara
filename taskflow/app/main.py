"""
TaskFlow - WhatsApp AI Task Automation Agent
Main FastAPI application with Twilio webhook integration.
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime
import pytz

from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import httpx

from .config import settings, get_log_file_path, get_memory_file_path
from .utils.logger import setup_logging
from .utils.rate_limiter import RateLimiter
from .utils.messages import get_welcome_message, get_help_message, get_friendly_error_message
from .agent import AgentOrchestrator
from .tools.reminder import ReminderTool
from .memory import MemoryStore


# Setup logging
logger = setup_logging()

# WhatsApp client (Meta or Twilio)
meta_client: Optional[MetaWhatsAppClient] = None
twilio_client: Optional[Client] = None
request_validator: Optional[RequestValidator] = None
use_meta: bool = False  # Flag to determine which service to use

# Agent orchestrator
agent: Optional[AgentOrchestrator] = None

# Reminder checker task
_reminder_checker_task: Optional[asyncio.Task] = None

# Rate limiter
rate_limiter: Optional[RateLimiter] = None

# IST timezone
IST = pytz.timezone('Asia/Kolkata')


async def check_reminders_loop(reminder_tool: ReminderTool, memory_store: MemoryStore):
    """
    Background task that checks for due reminders every minute.
    
    Args:
        reminder_tool: ReminderTool instance
        memory_store: MemoryStore instance
    """
    logger.info("🔄 Reminder checker loop started")
    
    while True:
        try:
            await asyncio.sleep(60)  # Check every minute
            
            # Get all pending reminders
            pending_reminders = memory_store.get_all_pending_reminders()
            
            if not pending_reminders:
                continue
            
            now_ist = datetime.now(IST)
            
            # Check each reminder
            for reminder in pending_reminders:
                try:
                    reminder_dt_str = reminder.get("datetime")
                    if not reminder_dt_str:
                        continue
                    
                    # Parse datetime
                    reminder_dt = datetime.fromisoformat(reminder_dt_str)
                    if reminder_dt.tzinfo is None:
                        reminder_dt = IST.localize(reminder_dt)
                    else:
                        reminder_dt = reminder_dt.astimezone(IST)
                    
                    # Check if reminder is due (within the last minute)
                    time_diff = (now_ist - reminder_dt).total_seconds()
                    
                    if 0 <= time_diff < 60:  # Due in the last minute
                        user_number = reminder.get("user_number")
                        reminder_id = reminder.get("id")
                        task = reminder.get("task", "Reminder")
                        
                        # Send reminder notification
                        message = (
                            f"⏰ REMINDER:\n"
                            f"📝 {task}\n\n"
                            f"Want me to snooze for 1 hour?"
                        )
                        
                        # Format user number for WhatsApp
                        if not user_number.startswith("whatsapp:"):
                            whatsapp_number = f"whatsapp:{user_number}"
                        else:
                            whatsapp_number = user_number
                        
                        success = await send_whatsapp_message(whatsapp_number, message)
                        
                        if success:
                            # Mark reminder as sent
                            memory_store.update_reminder(
                                user_number,
                                reminder_id,
                                {"status": "sent", "sent_at": now_ist.isoformat()}
                            )
                            logger.info(f"✅ Sent reminder to {user_number}: {task}")
                        else:
                            logger.error(f"❌ Failed to send reminder to {user_number}")
                
                except Exception as e:
                    logger.error(f"Error processing reminder: {e}", exc_info=True)
                    continue
                    
        except asyncio.CancelledError:
            logger.info("🔄 Reminder checker loop cancelled")
            break
        except Exception as e:
            logger.error(f"Error in reminder checker loop: {e}", exc_info=True)
            await asyncio.sleep(60)  # Wait before retrying


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Handles startup and shutdown events with optimizations for Render deployment.
    """
    import time
    startup_start = time.time()
    
    # Startup
    global twilio_client, request_validator, agent, _reminder_checker_task, rate_limiter, meta_client, use_meta
    
    logger.info("🚀 Starting TaskFlow application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Port: {settings.PORT}")
    
    # Initialize rate limiter (fast, in-memory)
    rate_limiter = RateLimiter(max_messages=10, window_seconds=60)
    logger.info("✅ Rate limiter initialized (10 messages/minute per user)")
    
    # Load memory at startup (preload for faster access)
    try:
        memory_store = MemoryStore()
        memory_store.load()  # Explicitly load to cache in memory
        logger.info("✅ Memory store preloaded")
    except Exception as e:
        logger.warning(f"⚠️  Could not preload memory store: {e}")
        memory_store = None
    
    # Initialize WhatsApp client (Meta or Twilio)
    use_meta = bool(settings.META_ACCESS_TOKEN and settings.PHONE_NUMBER_ID)
    
    if use_meta:
        # Use Meta WhatsApp Business API
        try:
            meta_client = MetaWhatsAppClient()
            logger.info("✅ Meta WhatsApp client initialized successfully")
            logger.info(f"   Phone Number ID: {settings.PHONE_NUMBER_ID}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Meta WhatsApp client: {e}")
            raise
    else:
        # Use Twilio (fallback)
        try:
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                raise ValueError("Either Meta or Twilio credentials must be provided")
            twilio_client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            request_validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            logger.info("✅ Twilio client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Twilio client: {e}")
            raise
    
    # Initialize Agent Orchestrator (caches Gemini client)
    try:
        agent = AgentOrchestrator()
        logger.info("✅ Agent orchestrator initialized successfully")
        
        # Preload Gemini client if available (cache for faster responses)
        if agent.gemini_model:
            logger.info("✅ Gemini client cached and ready")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent orchestrator: {e}")
        # Don't raise - allow app to start even if agent fails (for testing)
        logger.warning("⚠️  Continuing without agent (limited functionality)")
    
    # Preload Playwright browser (async, non-blocking)
    browser_preload_task = None
    if agent and hasattr(agent, 'price_tool'):
        try:
            price_tool = agent.price_tool
            if hasattr(price_tool, '_ensure_browser'):
                # Start browser preload in background (non-blocking)
                async def preload_browser():
                    try:
                        await price_tool._ensure_browser()
                        logger.info("✅ Playwright browser preloaded")
                    except Exception as e:
                        logger.debug(f"Browser preload skipped: {e}")
                
                browser_preload_task = asyncio.create_task(preload_browser())
        except Exception as e:
            logger.debug(f"Browser preload not available: {e}")
    
    # Start reminder checker background task
    try:
        if memory_store:
            reminder_tool = ReminderTool(memory_store=memory_store)
            _reminder_checker_task = asyncio.create_task(check_reminders_loop(reminder_tool, memory_store))
            logger.info("✅ Reminder checker started")
    except Exception as e:
        logger.error(f"❌ Failed to start reminder checker: {e}")
    
    startup_time = time.time() - startup_start
    logger.info(f"✅ TaskFlow is ready to receive messages! (Startup: {startup_time:.2f}s)")
    
    # Render requirement: must start in under 60 seconds
    if startup_time > 60:
        logger.warning(f"⚠️  Startup took {startup_time:.2f}s (Render requires <60s)")
    else:
        logger.info(f"✅ Startup time {startup_time:.2f}s meets Render requirement (<60s)")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down TaskFlow...")
    shutdown_start = time.time()
    
    # Save memory before exit
    try:
        if memory_store:
            memory_store.save()
            logger.info("✅ Memory saved to disk")
    except Exception as e:
        logger.error(f"❌ Failed to save memory: {e}")
    
    # Close Playwright browser
    try:
        if agent and hasattr(agent, 'price_tool'):
            price_tool = agent.price_tool
            if hasattr(price_tool, '_close_browser'):
                await price_tool._close_browser()
                logger.info("✅ Playwright browser closed")
            elif hasattr(price_tool, 'cleanup'):
                await price_tool.cleanup()
                logger.info("✅ Playwright browser cleaned up")
    except Exception as e:
        logger.debug(f"Browser close: {e}")
    
    # Cancel reminder checker task
    if _reminder_checker_task:
        _reminder_checker_task.cancel()
        try:
            await _reminder_checker_task
        except asyncio.CancelledError:
            pass
        logger.info("✅ Reminder checker stopped")
    
    # Cancel browser preload task if still running
    if browser_preload_task and not browser_preload_task.done():
        browser_preload_task.cancel()
        try:
            await browser_preload_task
        except (asyncio.CancelledError, Exception):
            pass
    
    # Close API connections (Twilio client cleanup)
    try:
        if twilio_client:
            # Twilio client doesn't need explicit close, but log it
            logger.info("✅ Twilio client connections closed")
    except Exception as e:
        logger.debug(f"Twilio cleanup: {e}")
    
    shutdown_time = time.time() - shutdown_start
    logger.info(f"✅ Graceful shutdown complete (Shutdown: {shutdown_time:.2f}s)")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="WhatsApp AI Task Automation Agent",
    lifespan=lifespan,
)

# Add CORS middleware (for Render health checks and potential webhooks)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_twilio_request(request: Request, form_data: dict) -> bool:
    """
    Validate that the request is actually from Twilio.
    
    Args:
        request: The FastAPI request object
        form_data: The form data from the request
        
    Returns:
        True if request is valid, False otherwise
    """
    if settings.DEBUG and settings.ENVIRONMENT == "development":
        # Skip validation in development mode
        logger.warning("⚠️  Skipping Twilio signature validation (development mode)")
        return True
    
    if not request_validator:
        logger.error("Request validator not initialized")
        return False
    
    # Get the URL and signature
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    
    # Validate the request
    is_valid = request_validator.validate(url, form_data, signature)
    
    if not is_valid:
        logger.warning(f"⚠️  Invalid Twilio signature for request from {request.client.host}")
    
    return is_valid


async def send_whatsapp_message(to: str, message: str) -> bool:
    """
    Send a WhatsApp message via Meta or Twilio.
    
    Args:
        to: Recipient's WhatsApp number (format: whatsapp:+1234567890 or 1234567890)
        message: Message content to send
        
    Returns:
        True if message sent successfully, False otherwise
    """
    global use_meta, meta_client, twilio_client
    
    try:
        if use_meta and meta_client:
            # Use Meta WhatsApp API
            return await meta_client.send_message(to, message, message_type="text")
        elif twilio_client:
            # Use Twilio (fallback)
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            logger.info(f"📤 Sending message via Twilio to {to}")
            
            message_response = twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=to
            )
            
            logger.info(f"✅ Message sent successfully. SID: {message_response.sid}")
            return True
        else:
            logger.error("❌ No WhatsApp client initialized")
            return False
        
    except Exception as e:
        logger.error(f"❌ Failed to send message to {to}: {e}")
        return False


async def process_incoming_message(from_number: str, message_body: str) -> str:
    """
    Process incoming WhatsApp message and generate response using AI agent.
    Includes rate limiting, welcome message, and help command handling.
    
    Args:
        from_number: Sender's WhatsApp number
        message_body: The message content
        
    Returns:
        Response message to send back
    """
    global agent, rate_limiter
    
    # Check rate limit
    if rate_limiter:
        is_allowed, rate_limit_message = rate_limiter.is_allowed(from_number)
        if not is_allowed:
            logger.warning(f"Rate limit exceeded for {from_number}")
            return rate_limit_message
    
    # Check for help command
    message_lower = message_body.lower().strip()
    if message_lower in ["help", "hi", "hello", "hey"]:
        return get_help_message()
    
    if not agent:
        logger.error("Agent not initialized - cannot process message")
        return get_friendly_error_message("initialization")
    
    # Check if first-time user and send welcome message
    user_memory = agent.memory_store.get_user_memory(from_number)
    conversation_history = user_memory.get("conversation_history", [])
    
    # If this is the first conversation, send welcome message first
    is_first_time = len(conversation_history) == 0
    
    # Use agent to process message
    try:
        response = await agent.process_message(from_number, message_body)
        
        # If first-time user, prepend welcome message
        if is_first_time:
            welcome_msg = get_welcome_message()
            return f"{welcome_msg}\n\n{response}"
        
        return response
    except Exception as e:
        logger.error(f"Error in agent processing: {e}", exc_info=True)
        return get_friendly_error_message("processing")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint.
    Checks memory file accessibility and API key configuration.
    """
    health_status = {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
        "whatsapp_provider": "meta" if use_meta else "twilio",
        "meta_configured": meta_client is not None if use_meta else None,
        "twilio_configured": twilio_client is not None if not use_meta else None,
    }
    
    # Check memory file accessibility
    try:
        memory_file = get_memory_file_path()
        health_status["memory_file_accessible"] = memory_file.exists() or memory_file.parent.exists()
        if memory_file.exists():
            health_status["memory_file_size"] = memory_file.stat().st_size
    except Exception as e:
        logger.warning(f"Memory file check failed: {e}")
        health_status["memory_file_accessible"] = False
        health_status["memory_file_error"] = str(e)
    
    # Check API keys configuration
    health_status["api_keys"] = {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "serpapi_configured": bool(settings.SERPAPI_KEY),
        "meta_configured": bool(settings.META_ACCESS_TOKEN and settings.PHONE_NUMBER_ID),
        "twilio_configured": bool(settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN),
    }
    
    # Determine overall status
    whatsapp_configured = (use_meta and meta_client) or (not use_meta and twilio_client)
    if not whatsapp_configured:
        health_status["status"] = "degraded"
        health_status["issues"] = ["WhatsApp not configured"]
    elif not health_status.get("memory_file_accessible", True):
        health_status["status"] = "degraded"
        health_status["issues"] = ["Memory file not accessible"]
    else:
        health_status["status"] = "healthy"
    
    return health_status


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    WhatsApp webhook endpoint (supports both Meta and Twilio).
    Receives incoming WhatsApp messages and processes them.
    """
    global use_meta, meta_client
    
    try:
        if use_meta and meta_client:
            # Handle Meta WhatsApp webhook
            return await handle_meta_webhook(request)
        else:
            # Handle Twilio WhatsApp webhook (legacy)
            return await handle_twilio_webhook(request)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing webhook: {e}", exc_info=True)
        return PlainTextResponse(content="", status_code=200)


async def handle_meta_webhook(request: Request) -> PlainTextResponse:
    """Handle Meta WhatsApp webhook requests."""
    global meta_client
    
    try:
        # Parse JSON body from Meta
        body = await request.json()
        logger.info("="*80)
        logger.info(f"📨 Incoming Meta WhatsApp message")
        logger.debug(f"Raw payload: {body}")
        
        # Parse the message
        parsed_message = meta_client.parse_incoming_message(body)
        
        if not parsed_message:
            logger.warning("⚠️  Could not parse Meta webhook message")
            return PlainTextResponse(content="", status_code=200)
        
        from_number = parsed_message["from"]
        message_body = parsed_message["body"]
        message_id = parsed_message.get("message_id", "unknown")
        
        logger.info(f"From: {from_number}")
        logger.info(f"Message ID: {message_id}")
        logger.info(f"Body: {message_body[:100]}...")
        
        # Process the message and generate response
        response_message = await process_incoming_message(from_number, message_body)
        
        # Send response back to user
        success = await send_whatsapp_message(from_number, response_message)
        
        if success:
            logger.info("✅ Message processed and response sent successfully")
        else:
            logger.error("❌ Failed to send response message")
        
        logger.info("="*80)
        
        # Meta expects 200 OK
        return PlainTextResponse(content="", status_code=200)
        
    except Exception as e:
        logger.error(f"❌ Error processing Meta webhook: {e}", exc_info=True)
        return PlainTextResponse(content="", status_code=200)


async def handle_twilio_webhook(request: Request) -> PlainTextResponse:
    """Handle Twilio WhatsApp webhook requests (legacy support)."""
    try:
        form_data = await request.form()
        From = form_data.get("From", "")
        Body = form_data.get("Body", "")
        MessageSid = form_data.get("MessageSid")
        NumMedia = form_data.get("NumMedia", "0")
        
        # Log incoming message
        logger.info("="*80)
        logger.info(f"📨 Incoming Twilio WhatsApp message")
        logger.info(f"From: {From}")
        logger.info(f"Message SID: {MessageSid}")
        logger.info(f"Body: {Body[:100]}...")
        logger.info(f"Media count: {NumMedia}")
        
        # Get all form data for signature validation
        form_dict = {
            "From": From,
            "Body": Body,
        }
        if MessageSid:
            form_dict["MessageSid"] = MessageSid
        if NumMedia:
            form_dict["NumMedia"] = NumMedia
        
        # Validate request is from Twilio
        if not validate_twilio_request(request, form_dict):
            logger.error("❌ Invalid Twilio signature - rejecting request")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid request signature"
            )
        
        # Check if message contains media
        if NumMedia and int(NumMedia) > 0:
            response_message = "📎 I received your media! Media handling will be added in future phases."
            await send_whatsapp_message(From, response_message)
            return PlainTextResponse(content="", status_code=200)
        
        # Process the message and generate response
        response_message = await process_incoming_message(From, Body)
        
        # Send response back to user
        success = await send_whatsapp_message(From, response_message)
        
        if success:
            logger.info("✅ Message processed and response sent successfully")
        else:
            logger.error("❌ Failed to send response message")
        
        logger.info("="*80)
        
        # Return empty response (Twilio expects 200 OK with empty body)
        return PlainTextResponse(content="", status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing Twilio webhook: {e}", exc_info=True)
        
        # Try to send error notification to user
        try:
            From = form_data.get("From", "")
            if From:
                error_message = get_friendly_error_message("general")
                await send_whatsapp_message(From, error_message)
        except:
            pass
        
        # Return 200 to Twilio to avoid retries
        return PlainTextResponse(content="", status_code=200)


@app.get("/webhook")
async def webhook_get(request: Request):
    """
    Handle GET requests to webhook.
    - Meta: Webhook verification (returns challenge)
    - Twilio: Status check
    """
    global use_meta, meta_client
    
    if use_meta and meta_client:
        # Meta webhook verification
        if meta_client.verify_webhook(request):
            challenge = meta_client.get_challenge(request)
            if challenge:
                logger.info("✅ Meta webhook verified - returning challenge")
                return PlainTextResponse(content=challenge, status_code=200)
            else:
                return PlainTextResponse(content="", status_code=200)
        else:
            logger.warning("⚠️  Meta webhook verification failed")
            raise HTTPException(status_code=403, detail="Verification failed")
    else:
        # Twilio status check
        return {"message": "TaskFlow webhook endpoint is active"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
