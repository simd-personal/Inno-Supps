"""
Configuration settings for Inno Supps
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/innosupps")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # Feature flags
    mock_mode: bool = os.getenv("CONFIG_MOCK_MODE", "true").lower() == "true"
    
    # Rate limiting
    rate_limit_emails_per_hour: int = 50
    rate_limit_api_calls_per_minute: int = 100
    
    # Email settings
    email_cooldown_hours: int = 48  # No more than one email to same prospect in 48 hours
    
    # Vector embeddings
    embedding_dimension: int = 1536  # OpenAI ada-002 dimension
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
