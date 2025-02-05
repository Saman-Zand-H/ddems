from typing import Optional
from uuid import UUID

from fastapi_users.schemas import BaseUserCreate, CreateUpdateDictModel
from pydantic import EmailStr


class UserCreate(BaseUserCreate):
    username: str
    first_name: str
    last_name: str


class UserRead(CreateUpdateDictModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserUpdate(CreateUpdateDictModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
