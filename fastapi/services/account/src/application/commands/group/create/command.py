from pydantic import Field
from src.application import Command


class GroupCreateCommand(Command):
    name: str = Field(..., min_length=1, max_length=255)
