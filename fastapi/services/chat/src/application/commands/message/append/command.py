from uuid import UUID

from src.application import Command


class MessageAppendCommand(Command):
    message_id: UUID
    message: str
