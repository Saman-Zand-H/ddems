from uuid import UUID

from fastapi_users import FastAPIUsers

from src.domain.models import User
from src.infrastructure.auth.jwt_cookie import get_backends

from .dependencies import get_user_manager

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    auth_backends := get_backends(),
)
