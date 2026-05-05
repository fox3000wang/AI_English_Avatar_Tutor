from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import create_chat_reply

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Annotated[Session, Depends(get_db)]) -> ChatResponse:
    reply = create_chat_reply(
        db=db,
        session_id=request.session_id,
        message=request.message,
    )
    return ChatResponse(reply=reply)
