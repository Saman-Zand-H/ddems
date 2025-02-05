import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "RpKbbUUuYUWPpanM1JhCzNnXG")

JWT_TTL = timedelta(minutes=15)
JWT_COOKIE_NAME = "jwt"
JWT_COOKIE_SECURE = False
JWT_COOKIE_HTTPONLY = True
JWT_COOKIE_SAMESITE = "Lax"

DATABASE_URL = os.environ.get("DATABASE_URL")
