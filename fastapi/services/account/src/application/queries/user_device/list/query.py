from typing import Optional

from src.application import Query


class ListUserDevice(Query):
    user_id: Optional[int] = None
    device_type: Optional[str] = None
