from pydantic import BaseModel
from src.domain.choices import FeedbackChoices


class FeedbackMessage(BaseModel):
    feedback: FeedbackChoices
