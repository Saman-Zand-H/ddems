import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(os.path.join(BASE_DIR.parent, "common"))

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "RpKbbUUuYUWPpanM1JhCzNnXG")

JWT_TTL = timedelta(minutes=15)
JWT_COOKIE_NAME = "jwt"
JWT_COOKIE_SECURE = False
JWT_COOKIE_HTTPONLY = True
JWT_COOKIE_SAMESITE = "Lax"

DATABASE_URL = os.environ.get("DATABASE_URL")

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_ALGORITHM = os.environ.get("AUTH0_ALGORITHM", "RS256")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_ISSUER = os.environ.get("AUTH0_ISSUER")
