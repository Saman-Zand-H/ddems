from abc import ABC
from typing import Generic, Type

from pydantic import BaseModel


class Command(ABC):
    pass


class CommandHandler[C: Command](ABC, Generic[C]):
    def handle(self, command: C) -> None:
        raise NotImplementedError


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

    def handle[C: Command, R: BaseModel](self, command: C, **kwargs) -> R:
        handler = self.get_handler(type(command))
        return handler(**kwargs).handle(command)
