from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.voice_chat import VoiceChatResponse
from app.services.voice_chat_service import create_voice_chat_reply

router = APIRouter(tags=["voice-chat"])

SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav"}


def is_supported_audio_filename(filename: str) -> bool:
    return any(filename.lower().endswith(extension) for extension in SUPPORTED_AUDIO_EXTENSIONS)


@router.post("/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(
    session_id: Annotated[int, Form()],
    db: Annotated[Session, Depends(get_db)],
    file: Annotated[UploadFile | None, File()] = None,
) -> VoiceChatResponse:
    if file is None:
        raise HTTPException(status_code=400, detail="Audio file is required")

    if not is_supported_audio_filename(file.filename or ""):
        raise HTTPException(status_code=400, detail="Only wav and mp3 audio files are supported")

    audio_bytes = await file.read()
    user_text, ai_text, audio_url = create_voice_chat_reply(
        db=db,
        session_id=session_id,
        audio_bytes=audio_bytes,
        filename=file.filename or "audio",
        content_type=file.content_type,
    )
    return VoiceChatResponse(
        user_text=user_text,
        ai_text=ai_text,
        audio_url=audio_url,
    )
