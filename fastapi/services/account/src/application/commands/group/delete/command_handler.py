from sqlalchemy import delete
from src.application import CommandHandler, command_reg
from src.domain.models import Group

from .command import GroupDeleteCommand


@command_reg.register(GroupDeleteCommand)
class GroupDeleteCommandHandler(CommandHandler[GroupDeleteCommand]):
    async def handle(self, command, session) -> None:
        await session.execute(delete(Group).where(Group.id == command.id))
