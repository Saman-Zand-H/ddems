from typing import List

from sqlalchemy import select
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
    ) -> List[Message]:
        stmt = select(Message).where(Message.conversation_id == query.conversation_id)
        return list(await session.execute(stmt))
