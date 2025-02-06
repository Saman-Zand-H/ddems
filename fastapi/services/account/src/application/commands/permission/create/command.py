from pydantic import Field
from src.application import Command


class PermissionCreateCommand(Command):
    code: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
