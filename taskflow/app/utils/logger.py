"""
Logging configuration for TaskFlow.
Provides structured logging to both file and console.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from ..config import settings, get_log_file_path


def setup_logging() -> logging.Logger:
    """
    Configure and return the application logger.
    
    Sets up logging to both console and file with rotation.
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("taskflow")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation (10MB max, keep 5 backups)
    try:
        log_file = get_log_file_path()
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not set up file logging: {e}")
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

