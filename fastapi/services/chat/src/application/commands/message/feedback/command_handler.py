from sqlalchemy import update
from src.application import CommandHandler, command_reg
from src.domain.models import Message

from .command import MessageFeedbackCommand


@command_reg(MessageFeedbackCommand)
class MessageFeedbackCommandHandler(CommandHandler[MessageFeedbackCommand]):
    async def handle(self, command, session):
        await session.execute(
            update(Message)
            .where(Message.uuid == command.message_id)
            .values(feedback=command.feedback.value),
        )
