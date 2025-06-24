# config/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///styleflex.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Token expiration settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)   # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)      # 1 day
