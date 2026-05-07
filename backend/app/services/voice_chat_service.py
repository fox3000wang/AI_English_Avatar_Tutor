from sqlalchemy.orm import Session

from app.services.asr_service import transcribe_audio
from app.services.chat_service import create_chat_reply, set_latest_ai_message_audio_url
from app.services.tts_service import synthesize_speech


def create_voice_chat_reply(
    db: Session,
    session_id: int,
    audio_bytes: bytes,
    filename: str,
    content_type: str | None = None,
) -> tuple[str, str, str]:
    user_text = transcribe_audio(
        audio_bytes=audio_bytes,
        filename=filename,
        content_type=content_type,
    )
    ai_text = create_chat_reply(
        db=db,
        session_id=session_id,
        message=user_text,
    )
    audio_url = synthesize_speech(ai_text)
    set_latest_ai_message_audio_url(
        db=db,
        session_id=session_id,
        audio_url=audio_url,
    )
    return user_text, ai_text, audio_url
