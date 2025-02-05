from functools import lru_cache

from config import settings
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)


def _get_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.JWT_TTL,
        algorithm="HS256",
    )


def _get_cookie_transport() -> CookieTransport:
    return CookieTransport(
        cookie_name=settings.JWT_COOKIE_NAME,
        cookie_max_age=settings.JWT_TTL,
        cookie_secure=settings.JWT_COOKIE_SECURE,
        cookie_httponly=settings.JWT_COOKIE_HTTPONLY,
        cookie_samesite=settings.JWT_COOKIE_SAMESITE,
    )


def _get_bearer_transport() -> BearerTransport:
    return BearerTransport(tokenUrl="/auth/jwt/login")


@lru_cache(maxsize=None)
def get_backends():
    return [
        AuthenticationBackend(
            name="cookie",
            get_strategy=_get_strategy,
            transport=_get_cookie_transport(),
        ),
        AuthenticationBackend(
            name="bearer",
            get_strategy=_get_strategy,
            transport=_get_bearer_transport(),
        ),
    ]
