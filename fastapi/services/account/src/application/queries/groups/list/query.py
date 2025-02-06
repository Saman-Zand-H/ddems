from typing import Optional

from src.application import Query


class GroupListQuery(Query):
    id: Optional[int] = None
