from abc import ABC
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from unit_of_work import AbstractBaseUnitOfWork


class Query(BaseModel):
    pass


Q = TypeVar("Q", bound=Query)
R = TypeVar("R")


class QueryHandler(ABC, Generic[Q, R]):
    def __init__(self, uow: AbstractBaseUnitOfWork):
        self.uow = uow

    async def handle(self, query: Q, session: AsyncSession) -> R:
        raise NotImplementedError

    async def execute(self, query: Q) -> R:
        async with self.uow.get_transaction() as session:
            return await self.handle(query, session)


class QueryRegistry(Generic[Q, R]):
    def __init__(self):
        self._handlers = {}

    def get_all(self):
        return self._handlers

    def register(
        self,
        query: Type[Q],
        query_handler: Type[QueryHandler] | None = None,
    ) -> Type[QueryHandler]:

        if query_handler:
            self._handlers[query] = query_handler
            return query_handler

        def wrapper(handler: Type[QueryHandler]):
            self._handlers[query] = handler
            return handler

        return wrapper

    def get_handler(self, query_type: Type[Q]) -> Type[QueryHandler]:
        return self._handlers[query_type]

    async def handle(self, query: Q, **kwargs) -> R:
        handler = self.get_handler(type(query))
        return await handler(**kwargs).execute(query)
