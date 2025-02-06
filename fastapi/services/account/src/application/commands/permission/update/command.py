from pydantic import Field
from src.application import Command


class PermissionUpdateCommand(Command):
    id: int
    code: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
