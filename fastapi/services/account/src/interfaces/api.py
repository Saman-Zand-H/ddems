from typing import Annotated

import user_agents
from cqrs.commands import CommandRegistry

from fastapi import APIRouter, Body, Depends, Request, Security
from src.application.commands.user_device.login.command import LoginUserDevice
from src.application.queries.user_device.list.query import ListUserDevice
from src.infrastructure.db.unit_of_work import UnitOfWork
from src.interfaces.dependencies import (
    get_command_registry,
    get_query_registry,
    get_uow,
)

from .dependencies import verify_token
from .schemas import UserDeviceId, UserDeviceLogin

router = APIRouter(prefix="/user_device")


@router.post("/")
def login(
    body: Annotated[UserDeviceLogin, Body],
    request: Request,
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> UserDeviceId:
    user_agent = user_agents.parse(request.headers.get("user-agent"))
    command = LoginUserDevice(
        ip_address=request.client.host,
        device_type=user_agent.device.family,
        operating_system=user_agent.os.family,
        browser_type=user_agent.browser.family,
        user_id=body.user_id,
    )
    command_reg.handle(command, uow=uow)


@router.get("/")
def list(
    user_id: Annotated[str, Security(verify_token())],
    query_reg: Annotated[CommandRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> list[UserDeviceId]:
    query = ListUserDevice(user_id=user_id)
    return query_reg.handle(query, uow=uow)
