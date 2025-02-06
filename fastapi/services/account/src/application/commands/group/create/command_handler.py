from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import Group

from .command import GroupCreateCommand


@command_reg.register(GroupCreateCommand)
class GroupCreateCommandHandler(CommandHandler[GroupCreateCommand]):
    async def execute(self, command) -> None:
        async with self.uow.get_transaction() as session:
            if errors := await self.clean(command, session):
                raise ValidationError(errors)

            group = Group(**command.model_dump())
            session.add(group)
            await session.commit()

            return group

    async def clean(self, command: GroupCreateCommand, session: AsyncSession):
        errors = []
        group_exists = await session.execute(
            select(exists().filter(Group.name == command.name))
        )

        if group_exists.scalar():
            errors.append({Group.name.name: "Group with this name already exists."})

        return errors
