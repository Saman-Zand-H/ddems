import asyncio
import uuid
from threading import Lock
from typing import Annotated, List

from config import settings
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
from src.application.commands.message.append.command import MessageAppendCommand
from src.application.commands.message.feedback.command import (
    ConversationFeedbackCommand,
)
from src.application.queries.conversation.list.query import ListConversationsQuery
from src.application.queries.conversation.messages.query import (
    QueryMessagesByConversationId,
)
from src.application.sse.chat.handler import receive_response
from src.domain.choices import MessageStatus, Role
from src.domain.models import Conversation, Message
from src.infrastructure.db.unit_of_work import UnitOfWork
from src.interfaces.dependencies import (
    get_command_registry,
    get_query_registry,
    get_uow,
)

from .schemas import (
    ConversationCreated,
    ConversationList,
    FeedbackMessage,
    MessageList,
    SendMessage,
)

router = APIRouter(prefix="conversation/")


conversation_lock = Lock()


@router.get("{conversation_id}/receive")
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
                    raise asyncio.CancelledError()

                if (
                    (latest_msg := msgs.items[0]).role == Role.USER
                    or latest_msg.status == MessageStatus.IN_PROGRESS.value
                ):
                    raise asyncio.CancelledError()

                try:
                    async for chunk in receive_response(latest_msg.message):
                        yield chunk

                    await command_reg.handle(
                        MessageAppendCommand(
                            message_id=latest_msg.id,
                            message=chunk,
                        ),
                        uow=uow,
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            await asyncio.sleep(settings.CHAT_SSE_INTERVAL)

    return EventSourceResponse(event_generator(conversation_id))


@router.post("")
async def init_conversation(
    body: Annotated[InitConversationCommand, Body],
    command_reg: Annotated[CommandRegistry, Depends(get_command_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> ConversationCreated:
    response: Conversation = await command_reg.handle(body, uow=uow)
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=ConversationCreated(id=response.id),
    )


@router.get("")
async def list_conversations(
    query_reg: Annotated[QueryRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> ConversationList:
    responses: List[Conversation] = await query_reg.handle(
        ListConversationsQuery(), uow=uow
    )
    return ConversationList(responses)


@router.get("{conversation_id}")
async def get_conversation(
    conversation_id: Annotated[uuid.UUID, Path],
    query_reg: Annotated[QueryRegistry, Depends(get_query_registry)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MessageList:
    results: List[Message] = await query_reg.handle(
        QueryMessagesByConversationId(conversation_id=conversation_id),
        uow=uow,
    )
    return MessageList(results.items)


@router.post("{message_id}/feedback")
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


@router.post("{conversation_id}")
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


@router.delete("{conversation_id}")
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
