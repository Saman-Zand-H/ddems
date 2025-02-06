from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractBaseUnitOfWork(ABC):
    def __init__(self):
        self.session: AsyncSession = self.get_async_session()

    @abstractmethod
    def get_async_session(self) -> AsyncSession:
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.rollback()
            raise

    async def rollback(self):
        await self.session.rollback()

    @asynccontextmanager
    async def get_transaction(
        self, *, commit=True
    ) -> AsyncGenerator[AsyncSession, None]:
        try:
            yield self.session
        except Exception as e:
            await self.rollback()
            raise e
        finally:
            commit and await self.commit()
