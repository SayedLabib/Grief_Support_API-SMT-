from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-2.0-flash")

# Create an instance of Settings to export
settings = Settings(
    app_env=os.getenv("APP_ENV", "development"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
    gemini_model="gemini-2.0-flash"
)





