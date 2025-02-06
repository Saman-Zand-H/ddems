from fastapi import APIRouter
from src.interfaces.schemas.users import UserCreate, UserRead, UserUpdate

from .api.group import group_router
from .users import auth_backends, fastapi_users

router = APIRouter()


for auth_backend in auth_backends:
    router.include_router(fastapi_users.get_auth_router(auth_backend), tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)
router.include_router(fastapi_users.get_verify_router(UserRead), tags=["auth"])
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
        requires_verification=True,
    ),
    tags=["users"],
)
router.include_router(group_router, tags=["groups"])
