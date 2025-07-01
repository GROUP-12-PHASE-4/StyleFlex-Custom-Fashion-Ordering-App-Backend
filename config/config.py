import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")


    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15) 
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)     

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///styleflex.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
