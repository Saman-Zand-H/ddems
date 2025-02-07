from sqlalchemy import delete
from src.application import CommandHandler, command_reg
from src.domain.models import Conversation

from .command import DeleteConversationCommand


@command_reg(DeleteConversationCommand)
class DeleteConversationHandler(CommandHandler[DeleteConversationCommand]):
    async def handle(self, command, session):
        stmt = delete(Conversation).where(Conversation.id == command.conversation_id)
        await session.execute(stmt)
