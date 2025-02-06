from typing import Optional

from src.application import Query


class PermissionListQuery(Query):
    id: Optional[int] = None
