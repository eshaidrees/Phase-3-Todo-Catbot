from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationBase(SQLModel):
    user_id: uuid.UUID = Field(index=True)  # Assuming user table exists
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"  # Explicitly set table name

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime