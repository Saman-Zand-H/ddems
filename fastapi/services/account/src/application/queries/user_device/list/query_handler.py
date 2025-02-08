from typing import Sequence

from sqlalchemy import select
from src.application import QueryHandler, query_reg
from src.domain.models import UserDevice

from .query import ListUserDevice


@query_reg.register(ListUserDevice)
class ListUserDeviceHandler(QueryHandler[ListUserDevice, Sequence[UserDevice]]):
    async def handle(self, query, session):
        stmt = select(UserDevice)
        if query.user_id:
            stmt = stmt.where(UserDevice.user_id == query.user_id)

        if query.device_type:
            stmt = stmt.where(UserDevice.device_type == query.device_type)

        result = await session.execute(stmt)
        return result.scalars().all()
