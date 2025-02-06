from enum import StrEnum


class FeedbackChoices(StrEnum):
    LIKED = "liked"
    DISLIKED = "disliked"


class MessageStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    SENT = "sent"
    ERROR = "error"


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
