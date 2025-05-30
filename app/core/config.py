# config.py

import os
from dotenv import load_dotenv

# loading the environment variables from .env file
load_dotenv()


class Settings:
    # project name
    PROJECT_NAME: str = "Treklyio"

    # API Keys
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # logging level
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    BASE_URL : str = os.getenv("BASE_URL", "https://serpapi.com/search")


    class Config:
        env_file = ".env"


settings = Settings()
