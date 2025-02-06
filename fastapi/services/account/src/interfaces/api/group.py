from typing import Annotated, List

from cqrs.commands import CommandRegistry
from cqrs.queries import QueryRegistry
from src.application.commands.group.create.command import GroupCreateCommand
from src.application.queries.groups.list.query import GroupListQuery
from src.domain.models import User
from unit_of_work import AbstractBaseUnitOfWork

from fastapi import APIRouter, Body, Depends

from ..decorators import superuser_only
from ..dependencies import get_command_registry, get_query_registry, get_uow
from ..schemas.groups import GroupCreate, GroupRead

group_router = APIRouter(prefix="/group")


@group_router.post("/")
@superuser_only
async def group_create(
    group: Annotated[GroupCreate, Body(...)],
    command_registry: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[AbstractBaseUnitOfWork, Depends(get_uow)],
) -> GroupRead:
    command = GroupCreateCommand(**group.model_dump())
    results: User = await command_registry.handle(command, uow=uow)

    return GroupRead(**results).model_dump()


@group_router.get("/")
async def group_read(
    query_registry: Annotated[
        QueryRegistry[GroupListQuery, List[GroupRead]], Depends(get_query_registry)
    ],
    uow: Annotated[AbstractBaseUnitOfWork, Depends(get_uow)],
) -> List[GroupRead]:
    query = GroupListQuery()
    results = await query_registry.handle(query, uow=uow)

    return results
