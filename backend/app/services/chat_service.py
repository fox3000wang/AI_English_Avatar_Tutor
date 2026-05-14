from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.chat_message import ChatMessage


def strip_thinking_text(text: str) -> str:
    if "</think>" in text:
        return text.split("</think>", 1)[1].strip()
    return text.strip()


def generate_reply(message: str) -> str:
    settings = get_settings()
    if settings.chat_provider == "minimax" and settings.minimax_api_key:
        return generate_minimax_reply(message)

    return f"That's interesting! Can you tell me more about {message}?"


def generate_minimax_reply(message: str) -> str:
    settings = get_settings()

    from openai import OpenAI

    client = OpenAI(
        api_key=settings.minimax_api_key,
        base_url=settings.minimax_base_url,
    )
    response = client.chat.completions.create(
        model=settings.minimax_chat_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a warm, encouraging English teacher for a child. "
                    "Reply in simple English."
                ),
            },
            {"role": "user", "content": message},
        ],
    )
    content = response.choices[0].message.content or "Great job! Can you say one more sentence?"
    return strip_thinking_text(content)


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
