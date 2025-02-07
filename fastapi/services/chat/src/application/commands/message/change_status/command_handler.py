from sqlalchemy import update
from src.application import CommandHandler, command_reg
from src.domain.models import Message

from .command import MessageChangeStatusCommand


@command_reg(MessageChangeStatusCommand)
class MessageChangeStatusCommandHandler(CommandHandler[MessageChangeStatusCommand]):
    async def handle(
        self,
        command,
        session,
    ) -> None:
        return await session.execute(
            update(Message)
            .where(Message.id == command.message_id)
            .values(
                status=command.status,
            )
        )
