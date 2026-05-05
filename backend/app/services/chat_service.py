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
