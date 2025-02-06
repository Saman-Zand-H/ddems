from uuid import UUID

from src.application import Command


class InitConversationCommand(Command):
    user_id: UUID
    message: str
