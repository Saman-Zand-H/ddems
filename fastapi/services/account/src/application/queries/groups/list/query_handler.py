from typing import List

from sqlalchemy import select
from src.application import QueryHandler, query_reg
from src.domain.models import Group

from .query import GroupListQuery


@query_reg.register(GroupListQuery)
class GroupListQueryHandler(QueryHandler[GroupListQuery, Group]):
    async def handle(self, query, session) -> List[Group]:
        if query.id:
            stmt = select(Group).where(Group.id == query.id)
            return list(await session.execute(stmt))

        return list(await session.execute(select(Group)))
