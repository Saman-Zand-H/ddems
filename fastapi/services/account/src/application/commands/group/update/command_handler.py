from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import Group, group_permission

from .command import GroupUpdateCommand


@command_reg.register(GroupUpdateCommand)
class GroupUpdateCommandHandler(CommandHandler[GroupUpdateCommand]):
    async def handle(self, command, session):
        if errors := await self.clean(command, session):
            raise ValidationError(errors)

        if not (command.name or command.permissions):
            return

        if command.name:
            await session.execute(
                update(Group).where(Group.id == command.id).values(name=command.name)
            )

        if command.permissions:
            await session.execute(
                delete(group_permission).where(
                    group_permission.c.group_id == command.id
                )
            )

            values = [
                {
                    group_permission.c.group_id.name: command.id,
                    group_permission.c.permission_id.name: permission_id,
                }
                for permission_id in command.permissions
            ]
            await session.execute(group_permission.insert().values(values))

    async def clean(self, command: GroupUpdateCommand, session: AsyncSession):
        errors = []
        group_exists = await session.execute(
            select(exists().filter(Group.id == command.id))
        )
        if not group_exists.scalar():
            errors.append({Group.id.name: "Group with this id does not exist."})

        if command.name:
            is_duplicate = await session.execute(
                select(exists().filter(Group.name == command.name))
            )
            if is_duplicate.scalar():
                errors.append({Group.name.name: "Group with this name already exists."})

        return errors
