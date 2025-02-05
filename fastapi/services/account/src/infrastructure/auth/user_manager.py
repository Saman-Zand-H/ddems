from uuid import UUID

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from src.domain.models import User

from fastapi import Depends

from ..db.connection import SessionLocal


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    pass


def get_user_db():
    yield SQLAlchemyUserDatabase(User, SessionLocal())


def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
