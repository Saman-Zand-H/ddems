from typing import Optional
from uuid import UUID

from src.application import Query


class ListConversationsQuery(Query):
    user_id: Optional[UUID] = None
