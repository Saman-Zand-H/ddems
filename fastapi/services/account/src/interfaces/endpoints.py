from uuid import UUID

from fastapi_users import FastAPIUsers

from fastapi import APIRouter
from src.domain.models import User
from src.infrastructure.auth.jwt_cookie import get_backends
from src.infrastructure.auth.user_manager import get_user_manager
from src.interfaces.schemas.users import UserCreate, UserRead, UserUpdate

router = APIRouter()

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    auth_backends := get_backends(),
)

for auth_backend in auth_backends:
    router.include_router(fastapi_users.get_auth_router(auth_backend), tags=["auth"])

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
        requires_verification=True,
    )
)
