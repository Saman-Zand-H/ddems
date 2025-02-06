from typing import Optional
from uuid import UUID

from pydantic import Field
from src.application import Command


class UserShallowUpdateCommand(Command):
    id: UUID
    username: Optional[str] = Field(None, max_length=50, min_length=1)
    first_name: Optional[str] = Field(None, max_length=50, min_length=1)
    last_name: Optional[str] = Field(None, max_length=50, min_length=1)
