from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship

from .choices import FeedbackChoices, MessageStatus, Role


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = sa.Column(
        sa.String(255),
        unique=True,
        nullable=False,
        default="New Conversation",
    )

    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "message"

    id = sa.Column(sa.Integer, primary_key=True)
    message = sa.Column(sa.Text, nullable=False, default="")
    role = sa.Column(
        sa.Enum(Role),
        nullable=False,
        default=Role.USER.value,
    )
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified_at = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    status = sa.Column(
        sa.Enum(MessageStatus),
        nullable=False,
        default=MessageStatus.PENDING,
    )
    conversation_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("conversations.id"),
        onupdate="CASCADE",
        nullable=False,
    )
    feedback = sa.Column(sa.Enum(FeedbackChoices), nullable=True)

    conversation = relationship("Conversation", back_populates="messages")
