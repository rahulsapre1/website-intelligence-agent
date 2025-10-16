from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str
    supabase_url: str
    supabase_key: str
    jina_api_key: str
    
    # Authentication
    api_secret_key: str
    
    # Rate Limiting
    rate_limit_per_minute: int = 10
    
    # App Settings
    app_name: str = "Website Intelligence Agent"
    debug: bool = False
    port: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()
