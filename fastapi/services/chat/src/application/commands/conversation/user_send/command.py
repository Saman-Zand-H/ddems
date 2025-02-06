from uuid import UUID

from src.application import Command


class UserSendCommand(Command):
    conversation_id: UUID
    message: str
