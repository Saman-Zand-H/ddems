from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from src.application import command_reg, query_reg
from src.domain.models import User
from src.infrastructure.auth.user_manager import UserManager
from src.infrastructure.db.connection import get_async_session_generator
from src.infrastructure.db.unit_of_work import UnitOfWork


async def get_uow():
    async with UnitOfWork() as uow:
        yield uow


async def get_user_db(session: AsyncSession = Depends(get_async_session_generator)):
    yield SQLAlchemyUserDatabase(session, User)


def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_query_registry():
    return query_reg


def get_command_registry():
    return command_reg
