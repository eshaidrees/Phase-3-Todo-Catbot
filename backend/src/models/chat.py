from pydantic import BaseModel
from typing import Optional
import uuid


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    conversation_id: str
    response: str
    timestamp: str
    operation: Optional[dict] = None


class ListConversationsResponse(BaseModel):
    success: bool
    conversations: list


class GetMessagesResponse(BaseModel):
    success: bool
    messages: list