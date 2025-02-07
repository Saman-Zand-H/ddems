from typing import List
from uuid import UUID

from pydantic import BaseModel, RootModel


class ConversationCreated(BaseModel):
    id: UUID


class ConversationRead(BaseModel):
    id: UUID
    title: str


ConversationList = RootModel[List[ConversationRead]]
