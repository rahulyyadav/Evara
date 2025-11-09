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
    
    # Meta (Facebook) WhatsApp Business API (Required)
    META_ACCESS_TOKEN: str = Field(..., env="META_ACCESS_TOKEN")
    PHONE_NUMBER_ID: str = Field(..., env="PHONE_NUMBER_ID")
    META_VERIFY_TOKEN: str = Field(..., env="META_VERIFY_TOKEN")
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
# Will raise ValidationError if required fields are missing
try:
    settings = Settings()
except Exception as e:
    import sys
    print(f"❌ Configuration Error: {e}", file=sys.stderr)
    print("\nPlease ensure all required environment variables are set:")
    print("  - META_ACCESS_TOKEN")
    print("  - PHONE_NUMBER_ID")
    print("  - META_VERIFY_TOKEN")
    print("\nOptional variables:")
    print("  - GEMINI_API_KEY (for AI features)")
    print("  - SERPAPI_KEY (for flight search)")
    print("  - WHATSAPP_BUSINESS_ID")
    print("  - ENVIRONMENT (dev/prod, defaults to dev)")
    print("  - LOG_LEVEL (defaults to INFO)")
    print("\nSee .env.example for template.")
    sys.exit(1)


def get_memory_file_path() -> Path:
    """Get the full path to the memory file."""
    return settings.DATA_DIR / settings.MEMORY_FILE


def get_log_file_path() -> Path:
    """Get the full path to the log file."""
    return settings.LOGS_DIR / "evara.log"
