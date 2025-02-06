from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, CreateUpdateDictModel


class UserCreate(BaseUserCreate):
    username: str
    first_name: str
    last_name: str


class UserRead(BaseUser):
    username: str
    first_name: str
    last_name: str


class UserUpdate(CreateUpdateDictModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
