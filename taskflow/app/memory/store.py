"""
Memory store for TaskFlow.
Handles persistent storage of user data and conversation history.
Enhanced with thread-safe operations, atomic writes, and backup system.
"""
import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import os
import sys

# Cross-platform file locking
try:
    if sys.platform == 'win32':
        import msvcrt
        _LOCK_AVAILABLE = True
        _LOCK_TYPE = 'windows'
    else:
        import fcntl
        _LOCK_AVAILABLE = True
        _LOCK_TYPE = 'unix'
except ImportError:
    _LOCK_AVAILABLE = False
    _LOCK_TYPE = None

from ..config import get_memory_file_path, settings

logger = logging.getLogger("taskflow")


class MemoryStore:
    """
    Manages user memory storage in JSON format.
    Stores conversation history, preferences, and task tracking.
    Thread-safe with atomic writes and backup system.
    """
    
    def __init__(self, memory_file: Optional[Path] = None):
        """
        Initialize memory store.
        
        Args:
            memory_file: Path to memory JSON file. If None, uses default from config.
        """
        self.memory_file = memory_file or get_memory_file_path()
        self._memory: Dict[str, Any] = {}
        self._lock_file = self.memory_file.with_suffix('.lock')
        self._backup_dir = self.memory_file.parent / "backups"
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        self._last_backup_date = None
        self._lock_fd = None
        
        self._load_memory()
        self._check_and_backup()
    
    def _acquire_lock(self):
        """Acquire file lock for thread-safe operations (cross-platform)."""
        if not _LOCK_AVAILABLE:
            return  # Skip locking if not available
        
        try:
            if self._lock_fd is None:
                self._lock_fd = open(self._lock_file, 'w')
            
            if _LOCK_TYPE == 'windows':
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_LOCK, 1)
            elif _LOCK_TYPE == 'unix':
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_EX)
        except Exception as e:
            logger.debug(f"Could not acquire file lock: {e}")
            # Continue without lock (better than failing)
            if self._lock_fd:
                try:
                    self._lock_fd.close()
                except:
                    pass
                self._lock_fd = None
    
    def _release_lock(self):
        """Release file lock."""
        if not _LOCK_AVAILABLE or self._lock_fd is None:
            return
        
        try:
            if _LOCK_TYPE == 'windows':
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
            elif _LOCK_TYPE == 'unix':
                fcntl.flock(self._lock_fd.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            logger.debug(f"Could not release file lock: {e}")
    
    def _load_memory(self) -> None:
        """Load memory from JSON file with error handling."""
        self._acquire_lock()
        try:
            if self.memory_file.exists():
                try:
                    with open(self.memory_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Migrate old format to new format if needed
                    if "users" not in data:
                        # Old format: flat structure
                        # New format: nested under "users"
                        self._memory = {
                            "users": data,
                            "version": "2.0",
                            "created_at": datetime.now().isoformat()
                        }
                        logger.info("Migrated memory from old format to new format")
                    else:
                        self._memory = data
                    
                    logger.debug(f"Loaded memory from {self.memory_file}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Corrupted JSON file: {e}")
                    # Try to load backup
                    backup = self._get_latest_backup()
                    if backup and backup.exists():
                        logger.info(f"Attempting to restore from backup: {backup}")
                        try:
                            with open(backup, 'r', encoding='utf-8') as f:
                                self._memory = json.load(f)
                            logger.info("Successfully restored from backup")
                        except Exception as backup_error:
                            logger.error(f"Backup also corrupted: {backup_error}")
                            self._memory = {"users": {}, "version": "2.0", "created_at": datetime.now().isoformat()}
                    else:
                        logger.warning("No backup available, starting fresh")
                        self._memory = {"users": {}, "version": "2.0", "created_at": datetime.now().isoformat()}
                except Exception as e:
                    logger.error(f"Failed to load memory: {e}")
                    self._memory = {"users": {}, "version": "2.0", "created_at": datetime.now().isoformat()}
            else:
                self._memory = {
                    "users": {},
                    "version": "2.0",
                    "created_at": datetime.now().isoformat()
                }
                logger.debug("No existing memory file found, starting fresh")
        finally:
            self._release_lock()
    
    def _save_memory(self) -> None:
        """Save memory to JSON file atomically with error handling."""
        self._acquire_lock()
        try:
            # Ensure directory exists
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Atomic write: write to temp file first, then rename
            temp_file = None
            try:
                # Create temp file in same directory
                temp_fd, temp_path = tempfile.mkstemp(
                    suffix='.json',
                    dir=self.memory_file.parent,
                    text=True
                )
                temp_file = Path(temp_path)
                
                # Write to temp file
                with open(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(self._memory, f, indent=2, ensure_ascii=False)
                
                # Atomic rename (works on Unix and Windows)
                temp_file.replace(self.memory_file)
                logger.debug(f"Saved memory atomically to {self.memory_file}")
                
            except OSError as e:
                if e.errno == 28:  # No space left on device
                    logger.error("Disk full! Cannot save memory.")
                    raise
                else:
                    logger.error(f"Failed to save memory: {e}")
                    raise
            except Exception as e:
                logger.error(f"Failed to save memory: {e}")
                # Clean up temp file if it exists
                if temp_file and temp_file.exists():
                    try:
                        temp_file.unlink()
                    except:
                        pass
                raise
                
        finally:
            self._release_lock()
    
    def _check_and_backup(self) -> None:
        """Check if daily backup is needed and create one."""
        try:
            today = datetime.now().date()
            
            # Check if we've backed up today
            if self._last_backup_date == today:
                return
            
            # Check if memory file exists and has content
            if not self.memory_file.exists():
                return
            
            # Create daily backup
            backup_filename = f"user_memory_{today.isoformat()}.json"
            backup_path = self._backup_dir / backup_filename
            
            # Only backup if file has changed or backup doesn't exist
            if not backup_path.exists() or self.memory_file.stat().st_mtime > backup_path.stat().st_mtime:
                try:
                    shutil.copy2(self.memory_file, backup_path)
                    self._last_backup_date = today
                    logger.info(f"Created daily backup: {backup_path}")
                    
                    # Clean up old backups (keep last 7 days)
                    self._cleanup_old_backups()
                except Exception as e:
                    logger.warning(f"Failed to create backup: {e}")
        except Exception as e:
            logger.warning(f"Error in backup check: {e}")
    
    def _cleanup_old_backups(self) -> None:
        """Remove backups older than 7 days."""
        try:
            cutoff_date = datetime.now().date() - timedelta(days=7)
            for backup_file in self._backup_dir.glob("user_memory_*.json"):
                try:
                    # Extract date from filename
                    date_str = backup_file.stem.replace("user_memory_", "")
                    backup_date = datetime.fromisoformat(date_str).date()
                    if backup_date < cutoff_date:
                        backup_file.unlink()
                        logger.debug(f"Removed old backup: {backup_file}")
                except Exception as e:
                    logger.debug(f"Could not parse backup date from {backup_file}: {e}")
        except Exception as e:
            logger.warning(f"Error cleaning up old backups: {e}")
    
    def _get_latest_backup(self) -> Optional[Path]:
        """Get the most recent backup file."""
        try:
            backups = list(self._backup_dir.glob("user_memory_*.json"))
            if not backups:
                return None
            # Sort by modification time, return most recent
            backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return backups[0]
        except Exception as e:
            logger.warning(f"Error finding latest backup: {e}")
            return None
    
    def _normalize_number(self, number: str) -> str:
        """
        Normalize phone number for consistent storage.
        Removes 'whatsapp:' prefix and normalizes format.
        
        Args:
            number: Phone number string
            
        Returns:
            Normalized phone number
        """
        # Remove whatsapp: prefix if present
        if number.startswith("whatsapp:"):
            number = number[9:]
        # Remove + if present (we'll store without it)
        if number.startswith("+"):
            number = number[1:]
        return number
    
    def _ensure_users_structure(self) -> None:
        """Ensure memory has the correct structure with 'users' key."""
        if "users" not in self._memory:
            # Migrate old structure
            old_data = self._memory.copy()
            self._memory = {
                "users": old_data,
                "version": "2.0",
                "created_at": datetime.now().isoformat()
            }
    
    def get_user_memory(self, user_number: str) -> Dict[str, Any]:
        """
        Get memory for a specific user.
        
        Args:
            user_number: User's phone number (normalized)
            
        Returns:
            User's memory dictionary
        """
        self._ensure_users_structure()
        normalized_number = self._normalize_number(user_number)
        users = self._memory.setdefault("users", {})
        
        if normalized_number not in users:
            users[normalized_number] = {
                "first_seen": datetime.now().isoformat(),
                "last_interaction": datetime.now().isoformat(),
                "preferences": {},
                "conversation_history": [],
                "tracked_products": [],
                "reminders": []
            }
        else:
            # Ensure existing user has all required fields (migration)
            user_data = users[normalized_number]
            if "first_seen" not in user_data:
                user_data["first_seen"] = user_data.get("created_at") or datetime.now().isoformat()
            if "last_interaction" not in user_data:
                user_data["last_interaction"] = user_data.get("last_updated") or datetime.now().isoformat()
            if "preferences" not in user_data:
                user_data["preferences"] = {}
            if "conversation_history" not in user_data:
                # Migrate from old format
                if "conversations" in user_data:
                    user_data["conversation_history"] = []
                    for old_conv in user_data.get("conversations", []):
                        user_data["conversation_history"].append({
                            "timestamp": old_conv.get("timestamp", datetime.now().isoformat()),
                            "user_message": old_conv.get("message", ""),
                            "agent_response": old_conv.get("response", ""),
                            "intent": old_conv.get("intent"),
                            "tool_used": None
                        })
                    del user_data["conversations"]
                else:
                    user_data["conversation_history"] = []
            if "tracked_products" not in user_data:
                # Migrate from old format
                if "tracked_items" in user_data:
                    user_data["tracked_products"] = user_data["tracked_items"]
                    del user_data["tracked_items"]
                else:
                    user_data["tracked_products"] = []
            if "reminders" not in user_data:
                user_data["reminders"] = []
        
        return users[normalized_number]
    
    def get_user_context(self, user_number: str) -> Dict[str, Any]:
        """
        Get full user context (alias for get_user_memory for Phase 6 compatibility).
        
        Args:
            user_number: User's phone number
            
        Returns:
            User's memory dictionary
        """
        return self.get_user_memory(user_number)
    
    def add_conversation(
        self,
        user_number: str,
        message: str,
        response: str,
        intent: Optional[str] = None,
        tool_used: Optional[str] = None
    ) -> None:
        """
        Add a conversation entry to user's memory.
        
        Args:
            user_number: User's phone number
            message: User's message
            response: Agent's response
            intent: Detected intent (optional)
            tool_used: Tool that was used (optional)
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "agent_response": response,
            "intent": intent,
            "tool_used": tool_used
        }
        
        # Support both old and new format for backward compatibility
        if "conversation_history" not in user_memory:
            # Migrate from old format if needed
            if "conversations" in user_memory:
                user_memory["conversation_history"] = []
                for old_conv in user_memory.get("conversations", []):
                    user_memory["conversation_history"].append({
                        "timestamp": old_conv.get("timestamp", datetime.now().isoformat()),
                        "user_message": old_conv.get("message", ""),
                        "agent_response": old_conv.get("response", ""),
                        "intent": old_conv.get("intent"),
                        "tool_used": None
                    })
                # Remove old format
                if "conversations" in user_memory:
                    del user_memory["conversations"]
            else:
                user_memory["conversation_history"] = []
        
        user_memory["conversation_history"].append(conversation_entry)
        user_memory["last_interaction"] = datetime.now().isoformat()
        
        # Keep only last 50 conversations to prevent file from growing too large
        if len(user_memory["conversation_history"]) > 50:
            user_memory["conversation_history"] = user_memory["conversation_history"][-50:]
        
        self._save_memory()
        self._check_and_backup()
    
    def save_conversation(
        self,
        user_number: str,
        message: str,
        response: str,
        intent: Optional[str] = None
    ) -> None:
        """
        Save conversation (alias for add_conversation for Phase 6 compatibility).
        
        Args:
            user_number: User's phone number
            message: User's message
            response: Agent's response
            intent: Detected intent (optional)
        """
        self.add_conversation(user_number, message, response, intent)
    
    def get_recent_conversations(self, user_number: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversation history for context.
        
        Args:
            user_number: User's phone number
            limit: Number of recent conversations to return
            
        Returns:
            List of recent conversation entries
        """
        user_memory = self.get_user_memory(user_number)
        # Support both old and new format
        conversations = user_memory.get("conversation_history") or user_memory.get("conversations", [])
        return conversations[-limit:] if conversations else []
    
    def update_preference(self, user_number: str, key: str, value: Any) -> None:
        """
        Update user preference.
        
        Args:
            user_number: User's phone number
            key: Preference key
            value: Preference value
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        user_memory["preferences"][key] = value
        user_memory["last_interaction"] = datetime.now().isoformat()
        self._save_memory()
    
    def update_preferences(self, user_number: str, prefs: Dict[str, Any]) -> None:
        """
        Update multiple user preferences at once.
        
        Args:
            user_number: User's phone number
            prefs: Dictionary of preferences to update
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        user_memory["preferences"].update(prefs)
        user_memory["last_interaction"] = datetime.now().isoformat()
        self._save_memory()
    
    def get_preference(self, user_number: str, key: str, default: Any = None) -> Any:
        """
        Get user preference.
        
        Args:
            user_number: User's phone number
            key: Preference key
            default: Default value if preference not found
            
        Returns:
            Preference value or default
        """
        user_memory = self.get_user_memory(user_number)
        return user_memory.get("preferences", {}).get(key, default)
    
    def add_tracked_product(self, user_number: str, product_data: Dict[str, Any]) -> str:
        """
        Add a tracked product for a user.
        
        Args:
            user_number: User's phone number
            product_data: Product data dictionary (must include id, title, url, current_price)
            
        Returns:
            Product ID
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        
        # Use tracked_products (Phase 6 format)
        if "tracked_products" not in user_memory:
            user_memory["tracked_products"] = []
        
        # Ensure product has required fields
        if "tracked_since" not in product_data:
            product_data["tracked_since"] = datetime.now().isoformat()
        if "last_checked" not in product_data:
            product_data["last_checked"] = datetime.now().isoformat()
        
        user_memory["tracked_products"].append(product_data)
        user_memory["last_interaction"] = datetime.now().isoformat()
        self._save_memory()
        
        return product_data.get("id", "")
    
    def get_tracked_products(self, user_number: str) -> List[Dict[str, Any]]:
        """
        Get all tracked products for a user.
        
        Args:
            user_number: User's phone number
            
        Returns:
            List of tracked product dictionaries
        """
        user_memory = self.get_user_memory(user_number)
        # Support both old and new format
        return user_memory.get("tracked_products") or user_memory.get("tracked_items", [])
    
    def update_tracked_product(self, user_number: str, product_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a tracked product.
        
        Args:
            user_number: User's phone number
            product_id: Product ID to update
            updates: Dictionary of fields to update
            
        Returns:
            True if product was found and updated, False otherwise
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        
        # Support both old and new format
        tracked_items = user_memory.get("tracked_products") or user_memory.get("tracked_items", [])
        
        # Migrate to new format if needed
        if "tracked_items" in user_memory and "tracked_products" not in user_memory:
            user_memory["tracked_products"] = user_memory["tracked_items"]
            del user_memory["tracked_items"]
            tracked_items = user_memory["tracked_products"]
        
        for item in tracked_items:
            if item.get("id") == product_id:
                item.update(updates)
                item["last_checked"] = datetime.now().isoformat()
                user_memory["last_interaction"] = datetime.now().isoformat()
                self._save_memory()
                return True
        
        return False
    
    def remove_tracked_product(self, user_number: str, product_id: str) -> bool:
        """
        Remove a tracked product.
        
        Args:
            user_number: User's phone number
            product_id: Product ID to remove
            
        Returns:
            True if product was found and removed, False otherwise
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        
        # Support both old and new format
        tracked_items = user_memory.get("tracked_products") or user_memory.get("tracked_items", [])
        
        # Migrate to new format if needed
        if "tracked_items" in user_memory and "tracked_products" not in user_memory:
            user_memory["tracked_products"] = user_memory["tracked_items"]
            del user_memory["tracked_items"]
            tracked_items = user_memory["tracked_products"]
        
        initial_count = len(tracked_items)
        user_memory["tracked_products"] = [item for item in tracked_items if item.get("id") != product_id]
        
        if len(user_memory["tracked_products"]) < initial_count:
            user_memory["last_interaction"] = datetime.now().isoformat()
            self._save_memory()
            return True
        
        return False
    
    def add_reminder(self, user_number: str, reminder_data: Dict[str, Any]) -> str:
        """
        Add a reminder for a user.
        
        Args:
            user_number: User's phone number
            reminder_data: Reminder data dictionary (must include id, task, datetime)
            
        Returns:
            Reminder ID
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        
        if "reminders" not in user_memory:
            user_memory["reminders"] = []
        
        # Ensure reminder has required fields
        if "status" not in reminder_data:
            reminder_data["status"] = "pending"
        if "created_at" not in reminder_data:
            reminder_data["created_at"] = datetime.now().isoformat()
        
        user_memory["reminders"].append(reminder_data)
        user_memory["last_interaction"] = datetime.now().isoformat()
        self._save_memory()
        
        return reminder_data.get("id", "")
    
    def get_reminders(self, user_number: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get reminders for a user.
        
        Args:
            user_number: User's phone number
            status: Optional status filter ("pending", "sent", "cancelled")
            
        Returns:
            List of reminder dictionaries
        """
        user_memory = self.get_user_memory(user_number)
        reminders = user_memory.get("reminders", [])
        
        if status:
            reminders = [r for r in reminders if r.get("status") == status]
        
        return reminders
    
    def get_all_pending_reminders(self) -> List[Dict[str, Any]]:
        """
        Get all pending reminders across all users.
        
        Returns:
            List of reminder dictionaries with user_number
        """
        self._ensure_users_structure()
        all_reminders = []
        users = self._memory.get("users", {})
        
        for user_number, user_data in users.items():
            reminders = user_data.get("reminders", [])
            for reminder in reminders:
                if reminder.get("status") == "pending":
                    reminder_with_user = reminder.copy()
                    reminder_with_user["user_number"] = user_number
                    all_reminders.append(reminder_with_user)
        
        return all_reminders
    
    def update_reminder(self, user_number: str, reminder_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a reminder.
        
        Args:
            user_number: User's phone number
            reminder_id: Reminder ID to update
            updates: Dictionary of fields to update
            
        Returns:
            True if reminder was found and updated, False otherwise
        """
        normalized_number = self._normalize_number(user_number)
        user_memory = self.get_user_memory(normalized_number)
        reminders = user_memory.get("reminders", [])
        
        for reminder in reminders:
            if reminder.get("id") == reminder_id:
                reminder.update(updates)
                user_memory["last_interaction"] = datetime.now().isoformat()
                self._save_memory()
                return True
        
        return False
    
    def cancel_reminder(self, user_number: str, reminder_id: str) -> bool:
        """
        Cancel a reminder.
        
        Args:
            user_number: User's phone number
            reminder_id: Reminder ID to cancel
            
        Returns:
            True if reminder was found and cancelled, False otherwise
        """
        return self.update_reminder(user_number, reminder_id, {"status": "cancelled"})
    
    def load(self) -> None:
        """Explicitly load memory from disk (Phase 6 compatibility)."""
        self._load_memory()
    
    def save(self) -> None:
        """Explicitly save memory to disk."""
        self._save_memory()
        self._check_and_backup()
