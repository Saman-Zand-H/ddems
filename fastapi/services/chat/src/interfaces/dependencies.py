import contextlib
from typing import Annotated

from config import settings
from jose import JWTError, jwt
from pydantic import ValidationError
from user_schema import StoredUser

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from src.application import command_reg, query_reg
from src.infrastructure.db.unit_of_work import UnitOfWork

auth_cookie = APIKeyCookie(name=settings.JWT_COOKIE_NAME)


async def get_uow():
    async with UnitOfWork() as uow:
        yield uow


def decode_jwt(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return StoredUser.model_validate(payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tampered token recognized.",
        )


def user_getter(suppress_exception: bool = False):
    def get_user(token: Annotated[str | None, Depends(auth_cookie)]):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided",
            )

        if suppress_exception:
            with contextlib.suppress(Exception):
                return decode_jwt(token)

        return decode_jwt(token)

    return get_user


def get_query_registry():
    return query_reg


def get_command_registry():
    return command_reg
