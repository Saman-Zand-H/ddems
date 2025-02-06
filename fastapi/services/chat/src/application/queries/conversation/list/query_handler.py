from typing import List

from sqlalchemy import select
from src.application import QueryHandler, query_reg
from src.domain.models import Conversation

from .query import ListConversationsQuery


@query_reg(ListConversationsQuery)
class ListConversationsQueryHandler(QueryHandler[ListConversationsQuery, Conversation]):
    async def handle(
        self,
        query,
        session,
    ) -> List[Conversation]:
        stmt = select(Conversation)
        if query.user:
            stmt = stmt.where(Conversation.user_id == query.user)
        return list(await session.execute(stmt))
