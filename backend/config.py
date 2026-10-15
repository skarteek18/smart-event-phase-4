

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    # Application settings
    APP_NAME = "SmartEvent"
    APP_VERSION = "4.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./smartevent.db"
    )

    # JWT authentication settings
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # AI chatbot configuration
    AI_API_KEY = os.getenv("AI_API_KEY", "")

    # Frontend configuration
    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )


settings = Settings()
