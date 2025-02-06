from functools import wraps
from typing import Annotated, Any, Callable

from config import settings
from user_schema import StoredUser

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie

from .dependencies import user_getter

auth_cookie = APIKeyCookie(name=settings.JWT_COOKIE_NAME)


def login_required(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[
            StoredUser | None, Depends(user_getter(suppress_exception=True))
        ],
        *args,
        **kwargs,
    ):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided",
            )

        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def superuser_only(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[StoredUser, Depends(user_getter())],
        *args,
        **kwargs,
    ):
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to perform this action",
            )

        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def verified_only(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[StoredUser, Depends(user_getter())],
        *args,
        **kwargs,
    ):
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to perform this action",
            )

        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def user_passes_test(test_func: Callable[[StoredUser], bool]):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(
            user: Annotated[
                StoredUser,
                Depends(user_getter()),
            ],
            *args,
            **kwargs,
        ):
            if not test_func(user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have permission to perform this action",
                )

            kwargs.update(user=user)
            return func(*args, **kwargs)

        return wrapper

    return decorator
