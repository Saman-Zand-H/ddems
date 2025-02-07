from uuid import UUID

from src.application import Command
from src.domain.choices import Role


class SendCommand(Command):
    conversation_id: UUID
    message: str
    role: Role = Role.USER.value
