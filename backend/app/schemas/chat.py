from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: int
    message: str


class ChatResponse(BaseModel):
    reply: str


class ChatMessageItem(BaseModel):
    id: int
    role: str
    text: str
    audio_url: str | None
    correction: str | None
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    session_id: int
    messages: list[ChatMessageItem]

