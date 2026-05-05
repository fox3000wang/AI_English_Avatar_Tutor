from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatMessageItem,
    ChatRequest,
    ChatResponse,
    VoiceChatResponse,
)
from app.services.chat_service import create_chat_reply, get_chat_history

router = APIRouter(tags=["chat"])

MOCK_ASR_TEXT = "Hello teacher"
MOCK_TTS_AUDIO_URL = "/audio/mock.mp3"


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Annotated[Session, Depends(get_db)]) -> ChatResponse:
    reply = create_chat_reply(
        db=db,
        session_id=request.session_id,
        message=request.message,
    )
    return ChatResponse(reply=reply)


@router.post("/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(
    session_id: Annotated[int, Form()],
    audio: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
) -> VoiceChatResponse:
    await audio.read()
    ai_text = create_chat_reply(
        db=db,
        session_id=session_id,
        message=MOCK_ASR_TEXT,
    )
    return VoiceChatResponse(
        user_text=MOCK_ASR_TEXT,
        ai_text=ai_text,
        audio_url=MOCK_TTS_AUDIO_URL,
    )


@router.get("/chat-history", response_model=ChatHistoryResponse)
async def chat_history(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> ChatHistoryResponse:
    messages = get_chat_history(db=db, session_id=session_id)
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[
            ChatMessageItem(
                id=message.id,
                role=message.role,
                text=message.text,
                audio_url=message.audio_url,
                correction=message.correction,
                created_at=message.created_at,
            )
            for message in messages
        ],
    )
