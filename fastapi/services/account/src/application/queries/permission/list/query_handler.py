from typing import List

from sqlalchemy import select
from src.application import QueryHandler, query_reg
from src.domain.models import Permission

from .query import PermissionListQuery


@query_reg.register(PermissionListQuery)
class PermissionListQueryHandler(QueryHandler[PermissionListQuery, Permission]):
    async def handle(self, query, session) -> List[Permission]:
        if query.id:
            stmt = select(Permission).where(Permission.id == query.id)
            return list(await session.execute(stmt))

        return list(await session.execute(select(Permission)))
