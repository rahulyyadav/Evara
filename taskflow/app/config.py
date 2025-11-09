"""
Configuration management for Evara.
Loads environment variables and provides centralized config access.
Uses pydantic BaseSettings for validation and type safety.
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Required variables:
    - META_ACCESS_TOKEN
    - PHONE_NUMBER_ID
    - META_VERIFY_TOKEN
    
    Optional variables:
    - GEMINI_API_KEY (for AI features)
    - SERPAPI_KEY (for flight search)
    - ENVIRONMENT (dev/prod, defaults to dev)
    - WHATSAPP_BUSINESS_ID (optional, for Meta integration)
    """
    
    # Application
    APP_NAME: str = "Evara"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="dev", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    @field_validator("PORT", mode="before")
    @classmethod
    def validate_port(cls, v):
        """Handle PORT from Render environment variable."""
        if v is None:
            # Try to get from environment (Render sets PORT)
            import os
            port_str = os.getenv("PORT")
            if port_str:
                try:
                    return int(port_str)
                except ValueError:
                    pass
        return v if v is not None else 8000
    
    # Meta (Facebook) WhatsApp Business API (Required for WhatsApp, but allow app to start without them)
    META_ACCESS_TOKEN: Optional[str] = Field(default=None, env="META_ACCESS_TOKEN")
    PHONE_NUMBER_ID: Optional[str] = Field(default=None, env="PHONE_NUMBER_ID")
    META_VERIFY_TOKEN: Optional[str] = Field(default=None, env="META_VERIFY_TOKEN")
    WHATSAPP_BUSINESS_ID: Optional[str] = Field(default=None, env="WHATSAPP_BUSINESS_ID")
    
    # Google Gemini API (Optional - for AI features)
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    
    # SerpAPI (Optional - for flight search)
    SERPAPI_KEY: Optional[str] = Field(default=None, env="SERPAPI_KEY")
    
    # Storage
    DATA_DIR: Path = Field(default=Path(__file__).parent.parent / "data")
    LOGS_DIR: Path = Field(default=Path(__file__).parent.parent / "logs")
    MEMORY_FILE: str = Field(default="user_memory.json", env="MEMORY_FILE")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        v_lower = v.lower()
        if v_lower not in ["dev", "development", "prod", "production"]:
            raise ValueError(f"ENVIRONMENT must be 'dev' or 'prod', got '{v}'")
        return v_lower
    
    @field_validator("DATA_DIR", "LOGS_DIR", mode="before")
    @classmethod
    def create_directories(cls, v) -> Path:
        """Ensure directories exist."""
        if isinstance(v, str):
            v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}, got '{v}'")
        return v_upper
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
# Allow app to start even if some env vars are missing (for health checks)
try:
    settings = Settings()
    # Warn if critical vars are missing but don't crash
    if not settings.META_ACCESS_TOKEN or not settings.PHONE_NUMBER_ID or not settings.META_VERIFY_TOKEN:
        import logging
        logger = logging.getLogger("taskflow")
        logger.warning("⚠️  Meta WhatsApp environment variables not fully configured:")
        if not settings.META_ACCESS_TOKEN:
            logger.warning("  - META_ACCESS_TOKEN is missing")
        if not settings.PHONE_NUMBER_ID:
            logger.warning("  - PHONE_NUMBER_ID is missing")
        if not settings.META_VERIFY_TOKEN:
            logger.warning("  - META_VERIFY_TOKEN is missing")
        logger.warning("  WhatsApp webhook will not work, but app will start for health checks.")
except Exception as e:
    import sys
    import logging
    logger = logging.getLogger("taskflow")
    logger.error(f"❌ Configuration Error: {e}")
    logger.error("App will start but may have limited functionality.")
    # Create minimal settings to allow app to start
    from pathlib import Path
    class MinimalSettings:
        APP_NAME = "Evara"
        APP_VERSION = "1.0.0"
        ENVIRONMENT = "prod"
        DEBUG = False
        HOST = "0.0.0.0"
        PORT = 8000
        META_ACCESS_TOKEN = None
        PHONE_NUMBER_ID = None
        META_VERIFY_TOKEN = None
        GEMINI_API_KEY = None
        SERPAPI_KEY = None
        MEMORY_FILE = "user_memory.json"
        DATA_DIR = Path(__file__).parent.parent / "data"
        LOGS_DIR = Path(__file__).parent.parent / "logs"
        # Ensure directories exist
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
    settings = MinimalSettings()


def get_memory_file_path() -> Path:
    """Get the full path to the memory file."""
    if hasattr(settings, 'DATA_DIR') and settings.DATA_DIR:
        return settings.DATA_DIR / settings.MEMORY_FILE
    # Fallback if DATA_DIR not set
    from pathlib import Path
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / settings.MEMORY_FILE


def get_log_file_path() -> Path:
    """Get the full path to the log file."""
    if hasattr(settings, 'LOGS_DIR') and settings.LOGS_DIR:
        return settings.LOGS_DIR / "evara.log"
    # Fallback if LOGS_DIR not set
    from pathlib import Path
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / "evara.log"
