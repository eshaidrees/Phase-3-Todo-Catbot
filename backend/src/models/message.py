from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(index=True)
    user_id: uuid.UUID = Field(index=True)
    role: str = Field(max_length=10)  # 'user' or 'assistant'
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None, nullable=True)  # Store as JSON string
    tool_responses: Optional[str] = Field(default=None, nullable=True)  # Store as JSON string


class Message(MessageBase, table=True):
    __tablename__ = "message"  # Explicitly set table name

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = None


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: uuid.UUID
    created_at: datetime