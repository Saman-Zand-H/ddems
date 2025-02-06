from sqlalchemy import delete
from src.application import CommandHandler, command_reg
from src.domain.models import Permission

from .command import PermissionDeleteCommand


@command_reg.register(PermissionDeleteCommand)
class PermissionDeleteCommandHandler(CommandHandler[PermissionDeleteCommand]):
    async def handle(self, command, session):
        await session.execute(delete(Permission).where(Permission.id == command.id))
