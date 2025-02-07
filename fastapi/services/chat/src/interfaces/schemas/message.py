from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, RootModel

from src.domain.choices import FeedbackChoices, MessageStatus, Role


class FeedbackMessage(BaseModel):
    feedback: FeedbackChoices


class MessageRead(BaseModel):
    id: UUID
    conversation_id: UUID
    message: str
    role: Role
    status: MessageStatus
    created_at: datetime
    modified_at: datetime
    feedback: FeedbackChoices


MessageList = RootModel[List[MessageRead]]


class SendMessage(BaseModel):
    message: str
