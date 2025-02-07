from uuid import UUID

from src.application import Command
from src.domain.choices import MessageStatus


class MessageChangeStatusCommand(Command):
    message_id: UUID
    status: MessageStatus
