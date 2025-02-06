from uuid import UUID

from src.application import Command


class UpdateConversationTitleCommand(Command):
    conversation_id: UUID
    title: str
