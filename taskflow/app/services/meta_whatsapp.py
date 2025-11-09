"""
Meta (Facebook) WhatsApp Business API integration.
Handles sending and receiving WhatsApp messages via Meta's Graph API.
"""
import logging
import httpx
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException

from ..config import settings

logger = logging.getLogger("taskflow")


class MetaWhatsAppClient:
    """
    Client for Meta WhatsApp Business API.
    Uses Graph API v22.0 for sending and receiving messages.
    """
    
    BASE_URL = "https://graph.facebook.com/v22.0"
    
    def __init__(self):
        """Initialize Meta WhatsApp client."""
        self.access_token = settings.META_ACCESS_TOKEN
        self.phone_number_id = settings.PHONE_NUMBER_ID
        self.whatsapp_business_id = settings.WHATSAPP_BUSINESS_ID
        
        if not all([self.access_token, self.phone_number_id]):
            raise ValueError("META_ACCESS_TOKEN and PHONE_NUMBER_ID must be set")
        
        self.api_url = f"{self.BASE_URL}/{self.phone_number_id}/messages"
        logger.info("✅ Meta WhatsApp client initialized")
    
    async def send_message(
        self,
        to: str,
        message: str,
        message_type: str = "text"
    ) -> bool:
        """
        Send a WhatsApp message using Meta's API.
        
        Args:
            to: Recipient phone number (format: 1234567890, no + or whatsapp: prefix)
            message: Message content
            message_type: Type of message (text, template, etc.)
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Clean phone number (remove +, whatsapp:, spaces)
            to_clean = to.replace("whatsapp:", "").replace("+", "").replace(" ", "").replace("-", "")
            
            logger.info(f"📤 Sending Meta WhatsApp message to {to_clean}")
            
            # Prepare payload according to Meta's API format
            if message_type == "text":
                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_clean,
                    "type": "text",
                    "text": {
                        "body": message
                    }
                }
            else:
                # For template messages
                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_clean,
                    "type": "template",
                    "template": {
                        "name": "hello_world",
                        "language": {
                            "code": "en_US"
                        }
                    }
                }
            
            # Send request to Meta API
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                result = response.json()
                
                if "messages" in result and len(result["messages"]) > 0:
                    message_id = result["messages"][0]["id"]
                    logger.info(f"✅ Message sent successfully. Message ID: {message_id}")
                    return True
                else:
                    logger.error(f"❌ Unexpected response format: {result}")
                    return False
                    
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_response = e.response.json()
                error_detail = error_response.get("error", {}).get("message", str(e))
            except:
                error_detail = str(e)
            
            logger.error(f"❌ Failed to send Meta WhatsApp message: {error_detail}")
            logger.debug(f"Response: {e.response.text}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to send Meta WhatsApp message: {e}", exc_info=True)
            return False
    
    def verify_webhook(self, request: Request) -> bool:
        """
        Verify webhook request from Meta (for webhook setup).
        
        Meta sends a GET request with:
        - hub.mode: "subscribe"
        - hub.verify_token: Your verify token
        - hub.challenge: Random string to echo back
        
        Args:
            request: FastAPI request object
            
        Returns:
            True if verification successful
        """
        try:
            mode = request.query_params.get("hub.mode")
            token = request.query_params.get("hub.verify_token")
            challenge = request.query_params.get("hub.challenge")
            
            verify_token = getattr(settings, "META_VERIFY_TOKEN", "taskflow_verify_token")
            
            if mode == "subscribe" and token == verify_token:
                logger.info("✅ Meta webhook verification successful")
                return True
            
            logger.warning(f"⚠️  Meta webhook verification failed: mode={mode}, token_match={token == verify_token}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error verifying Meta webhook: {e}")
            return False
    
    def get_challenge(self, request: Request) -> Optional[str]:
        """Get the challenge string from Meta webhook verification request."""
        return request.query_params.get("hub.challenge")
    
    def parse_incoming_message(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse incoming message from Meta webhook.
        
        Meta webhook format:
        {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "...",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {...},
                        "contacts": [...],
                        "messages": [{
                            "from": "1234567890",
                            "id": "...",
                            "timestamp": "...",
                            "type": "text",
                            "text": {
                                "body": "message content"
                            }
                        }]
                    }
                }]
            }]
        }
        
        Args:
            request_data: JSON data from Meta webhook
            
        Returns:
            Parsed message dict with 'from' and 'body' keys, or None if invalid
        """
        try:
            if request_data.get("object") != "whatsapp_business_account":
                return None
            
            entries = request_data.get("entry", [])
            if not entries:
                return None
            
            # Get first entry
            entry = entries[0]
            changes = entry.get("changes", [])
            if not changes:
                return None
            
            # Get first change
            change = changes[0]
            value = change.get("value", {})
            
            # Check if it's a message
            if "messages" not in value:
                return None
            
            messages = value.get("messages", [])
            if not messages:
                return None
            
            # Get first message
            message = messages[0]
            from_number = message.get("from")
            message_id = message.get("id")
            timestamp = message.get("timestamp")
            message_type = message.get("type")
            
            # Extract message body based on type
            body = ""
            if message_type == "text":
                body = message.get("text", {}).get("body", "")
            elif message_type == "image":
                body = "[Image received]"
            elif message_type == "document":
                body = "[Document received]"
            else:
                body = f"[{message_type} message]"
            
            if not from_number or not body:
                return None
            
            # Format phone number with whatsapp: prefix for consistency
            formatted_number = f"whatsapp:{from_number}"
            
            return {
                "from": formatted_number,
                "body": body,
                "message_id": message_id,
                "timestamp": timestamp,
                "type": message_type
            }
            
        except Exception as e:
            logger.error(f"❌ Error parsing Meta webhook message: {e}", exc_info=True)
            return None

