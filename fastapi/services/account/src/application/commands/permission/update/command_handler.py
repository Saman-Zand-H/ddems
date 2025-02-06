from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import Permission

from .command import PermissionUpdateCommand


@command_reg.register(PermissionUpdateCommand)
class PermissionUpdateCommandHandler(CommandHandler[PermissionUpdateCommand]):
    async def handle(self, command, session):
        if errors := await self.clean(command, session):
            raise ValidationError(errors)

        if not (command.name or command.code):
            return

        permission = await session.get(Permission, command.id)
        if command.name:
            permission.name = command.name

        if command.code:
            permission.code = command.code

        session.add(permission)

    async def clean(self, command: Permission, session: AsyncSession):
        errors = []
        permission_exists = await session.execute(
            select(exists().filter(Permission.id == command.id))
        )
        if not permission_exists.scalar():
            errors.append(
                {Permission.id.name: "Permission with this id does not exist."}
            )

        if command.name:
            is_duplicate_name = await session.execute(
                select(exists().filter(Permission.name == command.name))
            )
            if is_duplicate_name.scalar():
                errors.append(
                    {Permission.name.name: "Permission with this name already exists."}
                )

        if command.code:
            is_duplicate_code = await session.execute(
                select(exists().filter(Permission.code == command.code))
            )
            if is_duplicate_code.scalar():
                errors.append(
                    {Permission.code.name: "Permission with this code already exists."}
                )

        return errors
