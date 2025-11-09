"""
Rate limiting utility for TaskFlow.
Prevents spam by limiting messages per user per time window.
"""
import time
from typing import Dict, List
from collections import defaultdict
import logging

logger = logging.getLogger("taskflow")


class RateLimiter:
    """
    Simple in-memory rate limiter.
    Tracks message timestamps per user and enforces limits.
    """
    
    def __init__(self, max_messages: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_messages: Maximum number of messages allowed in the window
            window_seconds: Time window in seconds (default: 60 = 1 minute)
        """
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        # Store timestamps per user: {user_number: [timestamp1, timestamp2, ...]}
        self._user_timestamps: Dict[str, List[float]] = defaultdict(list)
        self._lock = {}  # Simple per-user lock (not thread-safe, but good enough for single process)
    
    def is_allowed(self, user_number: str) -> tuple[bool, str]:
        """
        Check if user is allowed to send a message.
        
        Args:
            user_number: User's phone number (normalized)
            
        Returns:
            Tuple of (is_allowed, message)
            - is_allowed: True if user can send message, False otherwise
            - message: Error message if not allowed, empty string if allowed
        """
        now = time.time()
        normalized_number = self._normalize_number(user_number)
        
        # Clean old timestamps outside the window
        cutoff_time = now - self.window_seconds
        timestamps = self._user_timestamps[normalized_number]
        self._user_timestamps[normalized_number] = [
            ts for ts in timestamps if ts > cutoff_time
        ]
        
        # Check if user has exceeded limit
        current_count = len(self._user_timestamps[normalized_number])
        
        if current_count >= self.max_messages:
            remaining_time = int(self.window_seconds - (now - self._user_timestamps[normalized_number][0]))
            if remaining_time < 0:
                remaining_time = 0
            return False, f"⏱️ Too many messages! Please wait {remaining_time} seconds before sending another message."
        
        # Add current timestamp
        self._user_timestamps[normalized_number].append(now)
        
        return True, ""
    
    def _normalize_number(self, number: str) -> str:
        """Normalize phone number for consistent storage."""
        if number.startswith("whatsapp:"):
            number = number[9:]
        if number.startswith("+"):
            number = number[1:]
        return number
    
    def reset_user(self, user_number: str) -> None:
        """Reset rate limit for a specific user (for testing/admin)."""
        normalized_number = self._normalize_number(user_number)
        if normalized_number in self._user_timestamps:
            del self._user_timestamps[normalized_number]
            logger.info(f"Reset rate limit for user {normalized_number}")
    
    def get_user_stats(self, user_number: str) -> Dict[str, int]:
        """Get rate limit stats for a user (for debugging)."""
        normalized_number = self._normalize_number(user_number)
        timestamps = self._user_timestamps.get(normalized_number, [])
        now = time.time()
        cutoff_time = now - self.window_seconds
        
        # Count messages in window
        messages_in_window = len([ts for ts in timestamps if ts > cutoff_time])
        
        return {
            "messages_in_window": messages_in_window,
            "max_messages": self.max_messages,
            "window_seconds": self.window_seconds
        }

