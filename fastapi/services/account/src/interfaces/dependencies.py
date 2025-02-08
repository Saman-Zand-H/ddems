from auth_dependency import VerifyToken
from config import settings

from fastapi import Security
from fastapi.security import APIKeyCookie
from src.application import command_reg, query_reg
from src.infrastructure.db.unit_of_work import UnitOfWork

auth_schema = APIKeyCookie(name=settings.JWT_COOKIE_NAME)


def verify_token(*scopes):
    def verify_token_decorator(token: str = Security(auth_schema)):
        return VerifyToken(settings).with_scopes(*scopes).verify(token)

    return verify_token_decorator


async def get_uow():
    async with UnitOfWork() as uow:
        yield uow


async def get_query_registry():
    return query_reg


async def get_command_registry():
    return command_reg
