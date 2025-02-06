from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr


class StoredUser(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    date_joined: datetime
    email: EmailStr
    username: str
    permissions: List[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
