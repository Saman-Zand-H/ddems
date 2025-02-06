from typing import List, Optional

from pydantic import Field
from src.application import Command


class GroupUpdateCommand(Command):
    id: int
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    permissions: Optional[List[int]] = None
