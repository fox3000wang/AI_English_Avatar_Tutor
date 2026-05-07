from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


def generate_reply(message: str) -> str:
    return f"That's interesting! Can you tell me more about {message}?"


def create_chat_reply(db: Session, session_id: int, message: str) -> str:
    reply = generate_reply(message)

    db.add_all(
        [
            ChatMessage(session_id=session_id, role="child", text=message),
            ChatMessage(session_id=session_id, role="ai", text=reply),
        ]
    )
    db.commit()

    return reply


def set_latest_ai_message_audio_url(db: Session, session_id: int, audio_url: str) -> None:
    message = db.scalars(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id, ChatMessage.role == "ai")
        .order_by(ChatMessage.id.desc())
    ).first()
    if message is None:
        return

    message.audio_url = audio_url
    db.commit()


def get_chat_history(db: Session, session_id: int) -> list[ChatMessage]:
    return list(
        db.scalars(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id)
        ).all()
    )
