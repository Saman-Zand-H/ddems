from sqlalchemy import func, update
from src.application import CommandHandler, command_reg
from src.domain.models import Message

from .command import MessageAppendCommand


@command_reg(MessageAppendCommand)
class MessageAppendCommandHandler(CommandHandler[MessageAppendCommand]):
    async def handle(
        self,
        command,
        session,
    ) -> None:
        return await session.execute(
            update(Message)
            .where(Message.id == command.message_id)
            .values(
                message=func.concat(Message.message, command.message),
            )
        )
