from uuid import UUID

from src.application import Command
from src.domain.choices import FeedbackChoices


class MessageFeedbackCommand(Command):
    message_id: UUID
    feedback: FeedbackChoices
