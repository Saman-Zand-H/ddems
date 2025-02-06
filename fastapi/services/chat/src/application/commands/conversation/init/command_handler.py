from sqlalchemy import insert
from src.application import CommandHandler, command_reg
from src.domain.choices import Role
from src.domain.models import Conversation, Message

from .command import InitConversationCommand


@command_reg(InitConversationCommand)
class InitConversationCommandHandler(
    CommandHandler[InitConversationCommand, Conversation]
):
    async def handle(
        self,
        command,
        session,
    ) -> Conversation:
        stmt = (
            insert(Conversation).values(user_id=command.user_id).returning(Conversation)
        )
        conversation = (await session.execute(stmt)).first()
        stmt = insert(Message).values(
            conversation_id=conversation.id,
            message=command.message,
            role=Role.USER.value,
        )
        await session.execute(stmt)
        return conversation
