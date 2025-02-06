from unit_of_work import AbstractBaseUnitOfWork

from .connection import get_async_session


class UnitOfWork(AbstractBaseUnitOfWork):
    def get_async_session(self):
        return get_async_session()
