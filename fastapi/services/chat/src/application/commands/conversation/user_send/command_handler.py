from sqlalchemy import insert
from src.application import CommandHandler, command_reg
from src.domain.choices import MessageStatus
from src.domain.models import Message

from .command import UserSendCommand


@command_reg(UserSendCommand)
class UserSendCommandHandler(CommandHandler[UserSendCommand, Message]):
    async def handle(
        self,
        command,
        session,
    ) -> Message:
        stmt = (
            insert(Message)
            .values(
                conversation_id=command.conversation_id,
                message=command.message,
                status=MessageStatus.SENT.value,
            )
            .returning(Message)
        )
        return (await session.execute(stmt)).first()
