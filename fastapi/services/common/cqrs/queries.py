from abc import ABC
from typing import Generic, Type

from pydantic import BaseModel


class Query(ABC):
    pass


class QueryHandler[Q: Query, R: BaseModel](ABC, Generic[Q, R]):
    def handle(self, query: Q) -> R:
        raise NotImplementedError


class QueryRegistry:
    def __init__(self):
        self._handlers = {}

    def register[
        Q: Query, QH: QueryHandler
    ](self, query: Type[Q], query_handler: Type[QH] | None = None) -> Type[QH]:
        if query_handler:
            self._handlers[query] = query_handler
            return query_handler

        def wrapper(handler: Type[QH]):
            self._handlers[query] = handler
            return handler

        return wrapper

    def get_handler[Q: Query](self, query_type: Type[Q]) -> Type[QueryHandler]:
        return self._handlers[query_type]

    def handle[Q: Query, R: BaseModel](self, query: Q, **kwargs) -> R:
        handler = self.get_handler(type(query))
        return handler(**kwargs).handle(query)
