from uuid import UUID

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models import User

from fastapi import Depends

from ..db.connection import get_async_session


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    def on_after_request_verify(self, user, token, request=None):
        print(f"User {user.id} has been verified with token {token}.")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
