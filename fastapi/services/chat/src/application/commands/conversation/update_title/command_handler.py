from sqlalchemy import exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import Conversation

from .command import UpdateConversationTitleCommand


@command_reg(UpdateConversationTitleCommand)
class UpdateConversationTitleCommandHandler(
    CommandHandler[UpdateConversationTitleCommand],
):
    async def handle(self, command, session):
        if errors := await self.clean(command, session):
            raise ValidationError(errors)

        stmt = (
            update(Conversation)
            .where(Conversation.id == command.conversation_id)
            .values(title=command.title)
            .returning(Conversation)
        )
        return (await session.execute(stmt)).first()

    async def clean(
        self,
        command: UpdateConversationTitleCommand,
        session: AsyncSession,
    ):
        errors = []

        conversation_exists = await session.execute(
            select(exists().where(Conversation.id == command.conversation_id))
        )
        if not conversation_exists.scalar():
            errors.append(
                f"Conversation with id {command.conversation_id} does not exist."
            )

        return errors
