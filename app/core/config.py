# core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""

    PROJECT_NAME: str = "Trekly"
    API_VERSION: str = "/api/v1"
    GEMINI_API_KEY: str
    SERPAPI_API_KEY: str
    MODEL_ID : str ="gemini-2.0-flash-lite"

    class Config:
        """Configuration for Pydantic settings."""
        env_file = ".env"


settings = Settings()
