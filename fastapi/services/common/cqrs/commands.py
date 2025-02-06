from abc import ABC
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from unit_of_work import AbstractBaseUnitOfWork


class Command(BaseModel):
    pass


C = TypeVar("C", bound=Command)


class CommandHandler(ABC, Generic[C]):

    def __init__(self, uow: AbstractBaseUnitOfWork):
        self.uow = uow

    async def handle(self, command: C, session: AsyncSession) -> None:
        raise NotImplementedError

    async def execute(self, command: C) -> None:
        async with self.uow.get_transaction() as session:
            return await self.handle(command, session)


class CommandRegistry:
    def __init__(self):
        self._handlers = {}

    def register[
        C: Command, CH: CommandHandler
    ](self, command: Type[C], command_handler: Type[CH] | None = None) -> Type[CH]:
        if command_handler:
            self._handlers[command] = command_handler
            return command_handler

        def wrapper(handler: Type[CH]):
            self._handlers[command] = handler
            return handler

        return wrapper

    def get_handler[C: Command](self, command: Type[C]) -> Type[CommandHandler]:
        return self._handlers[command]

    async def handle[C: Command, R: BaseModel](self, command: C, **kwargs) -> R:
        handler = self.get_handler(type(command))
        return await handler(**kwargs).execute(command)
