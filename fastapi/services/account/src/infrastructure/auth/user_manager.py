from uuid import UUID

from fastapi_users import BaseUserManager, UUIDIDMixin
from src.domain.models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    def on_after_request_verify(self, user, token, request=None):
        print(f"User {user.id} has been verified with token {token}.")
