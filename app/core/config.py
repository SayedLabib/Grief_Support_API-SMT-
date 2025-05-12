from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    groq_api_key: str = Field(default="")
    gemini_api_key: str = Field(default="")  # Add this if not already present
    youtube_api_key: str = Field(default="")

# Create an instance of Settings to export
settings = Settings(
    app_env=os.getenv("APP_ENV", "development"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    groq_api_key=os.getenv("GROQ_API_KEY", ""),
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),  # Add this if not already present
    youtube_api_key=os.getenv("YOUTUBE_API_KEY", "")
)





