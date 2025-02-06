from functools import wraps
from typing import Annotated, Any, Callable

from fastapi import Depends, HTTPException, status
from src.domain.models import User

from .users import fastapi_users


def login_required(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[
            User, Depends(fastapi_users.current_user(optional=True, active=True))
        ],
        *args,
        **kwargs
    ):
        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def superuser_only(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[
            User, Depends(fastapi_users.current_user(superuser=True, active=True))
        ],
        *args,
        **kwargs
    ):
        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def verified_only(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(
        user: Annotated[
            User, Depends(fastapi_users.current_user(verified=True, active=True))
        ],
        *args,
        **kwargs
    ):
        kwargs.update(user=user)
        return func(*args, **kwargs)

    return wrapper


def user_passes_test(test_func: Callable[[User], bool]):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(
            user: Annotated[
                User,
                Depends(fastapi_users.current_user(optional=True, active=True)),
            ],
            *args,
            **kwargs
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
