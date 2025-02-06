from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import CommandHandler, command_reg
from src.application.exceptions import ValidationError
from src.domain.models import Permission

from .command import PermissionCreateCommand


@command_reg.register(PermissionCreateCommand)
class PermissionCreateCommandHandler(CommandHandler[PermissionCreateCommand]):
    async def handle(self, command, session):
        if errors := await self.clean(command, session):
            raise ValidationError(errors)

        permission = Permission(**command.model_dump())
        session.add(permission)

    async def clean(self, command: PermissionCreateCommand, session: AsyncSession):
        errors = []

        permission_name_exists = await session.execute(
            select(exists().where(Permission.name == command.name))
        )
        if permission_name_exists.scalar():
            errors.append({Permission.name: "Permission with this name already exists"})

        permission_code_exists = await session.execute(
            select(exists().where(Permission.code == command.code))
        )
        if permission_code_exists.scalar():
            errors.append({Permission.code: "Permission with this code already exists"})

        return errors
