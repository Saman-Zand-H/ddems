# src/domain/services/auth_service.py
from datetime import datetime, timedelta

from config import settings
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256

from .constants import JWT_ALGORITHM


class AuthService:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def hash_password(password: str):
        return pbkdf2_sha256.hash(password, salt=settings.SECRET_KEY)

    @staticmethod
    def check_password(plain_password: str, hashed_password: str):
        return pbkdf2_sha256.verify(plain_password, hashed_password)
