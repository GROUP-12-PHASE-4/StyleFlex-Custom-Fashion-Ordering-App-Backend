# config/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Short-lived token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)     # Longer-lived token

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///styleflex.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
