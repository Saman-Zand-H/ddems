from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import User

from .command import UserShallowUpdateCommand


@command_reg.register(UserShallowUpdateCommand)
class UserShallowUpdateCommandHandler(CommandHandler[UserShallowUpdateCommand]):
    async def handle(self, command, session):
        if errors := await self.clean(command, session):
            raise ValidationError(errors)

        if not any(command.first_name, command.last_name, command.username):
            return

        user = await session.get(User, command.id)

        if command.first_name:
            user.first_name = command.first_name

        if command.last_name:
            user.last_name = command.last_name

        if command.username:
            user.username = command.username

        await session.add(user)

    async def clean(self, command: UserShallowUpdateCommand, session: AsyncSession):
        errors = []
        user_exists = await session.execute(select(User).filter(User.id == command.id))
        if not user_exists.scalar():
            errors.append("No user found with the given id.")

        if command.username:
            is_duplicate = await session.execute(
                select(exists().where(User.username == command.username))
            )
            if is_duplicate.scalar():
                errors.append({User.username.name: "Username already taken."})

        return errors
