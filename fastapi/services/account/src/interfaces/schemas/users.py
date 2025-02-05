from typing import Optional
from uuid import UUID

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import ConfigDict, EmailStr


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str


class UserRead(CreateUpdateDictModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(CreateUpdateDictModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
