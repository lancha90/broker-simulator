import logging
import os
import ssl

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    alphavantage_api_key: str = os.getenv("ALPHAVANTAGE_API_KEY", "")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Configure SSL verification based on environment variable
ssl_verify = os.getenv("SSL_VERIFY", "true").lower() == "true"

if not ssl_verify:
    logging.warning("SSL verification disabled - using unverified SSL context")
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    logging.info("SSL verification enabled - using default SSL context")
