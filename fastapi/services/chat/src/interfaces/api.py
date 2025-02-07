import asyncio
import uuid
from threading import Lock
from typing import Annotated

from cqrs.commands import CommandRegistry
from cqrs.queries import QueryRegistry
from fastapi_pagination import Page

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Response,
    status,
)
from fastapi.responses import EventSourceResponse
from src.application.commands.conversation.delete.command import (
    DeleteConversationCommand,
)
from src.application.commands.conversation.init.command import InitConversationCommand
from src.application.commands.conversation.send.command import SendCommand
from src.application.commands.message.feedback.command import (
    ConversationFeedbackCommand,
)
from src.application.queries.conversation.list.query import ListConversationsQuery
from src.application.queries.conversation.messages.query import (
    QueryMessagesByConversationId,
)
from src.application.sse.chat.handler import receive_response
from src.domain.choices import MessageStatus, Role
from src.domain.models import Message
from src.infrastructure.db.unit_of_work import UnitOfWork
from src.interfaces.dependencies import (
    get_command_registry,
    get_query_registry,
    get_uow,
)

from .schemas import FeedbackMessage, SendMessage

app = APIRouter(prefix="conversation/")


conversation_lock = Lock()


@app.get("{conversation_id}/message/receive")
async def start_conversation(
    conversation_id: Annotated[uuid.UUID, Path],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    query_reg: Annotated[QueryRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    async def event_generator(conversation_id: uuid.UUID):
        while True:
            with conversation_lock:
                msgs: Page[Message] = await query_reg.handle(
                    QueryMessagesByConversationId(
                        conversation_id=conversation_id,
                        page=1,
                        size=1,
                        order_by=f"-{Message.created_at.name}",
                    ),
                    uow=uow,
                )

                if not msgs.items:
                    ...

                if (
                    (latest_msg := msgs.items[0]).role == Role.USER
                    or latest_msg.status == MessageStatus.IN_PROGRESS.value
                ):
                    ...

                try:
                    async for chunk in receive_response("hi"):
                        yield chunk
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator(conversation_id))


@app.post("")
async def init_conversation(
    body: Annotated[InitConversationCommand, Body],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    return await command_reg.handle(body, uow=uow)


@app.get("")
def list_conversations(
    query_reg: Annotated[QueryRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    return query_reg.handle(ListConversationsQuery(), uow=uow)


@app.get("{conversation_id}")
def get_conversation(
    conversation_id: Annotated[uuid.UUID, Path],
    query_reg: Annotated[QueryRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    return query_reg.handle(
        QueryMessagesByConversationId(conversation_id=conversation_id),
        uow=uow,
    )


@app.post("{message_id}/feedback")
async def conversation_feedback(
    message_id: Annotated[uuid.UUID, Path],
    body: Annotated[FeedbackMessage, Body],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    await command_reg.handle(
        ConversationFeedbackCommand(
            message_id=message_id,
            feedback=body.feedback,
        ),
        uow=uow,
    )
    return Response()


@app.post("{conversation_id}")
async def send_message(
    conversation_id: Annotated[uuid.UUID, Path],
    message: Annotated[SendMessage, Body()],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    await command_reg.handle(
        SendCommand(
            conversation_id=conversation_id,
            message=message.message,
            role=Role.USER.value,
        ),
        uow=uow,
    )
    return Response(status_code=status.HTTP_201_CREATED)


@app.delete("{conversation_id}")
async def delete_conversation(
    conversation_id: Annotated[uuid.UUID, Path],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    await command_reg.handle(
        DeleteConversationCommand(conversation_id=conversation_id),
        uow=uow,
    )
    return Response()
