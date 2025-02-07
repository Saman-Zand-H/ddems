from typing import List

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc, select
from src.application import QueryHandler, query_reg
from src.domain.models import Message

from .query import QueryMessagesByConversationId


@query_reg(QueryMessagesByConversationId)
class QueryMessagesByConversationIdHandler(
    QueryHandler[QueryMessagesByConversationId, List[Message]],
):
    async def handle(
        self,
        query,
        session,
    ) -> List[Message] | Page[Message]:
        stmt = select(Message).where(Message.conversation_id == query.conversation_id)
        if query.role:
            stmt = stmt.where(Message.role == query.role.value)

        if not query.page:
            return list(await session.execute(stmt))

        if query.order_by:
            base_stmt = stmt.order_by(query.order_by).asc
            stmt = query.order_by.startswith("-") and desc(base_stmt) or base_stmt

        return await paginate(
            session,
            stmt,
            Params(page=query.page, size=query.size),
        )
