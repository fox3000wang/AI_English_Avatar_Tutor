from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.session import Base, get_db
from app.main import app
from app.models.chat_message import ChatMessage


def test_chat_api_returns_mock_reply_and_stores_messages() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/chat",
            json={"session_id": 1, "message": "Hello teacher"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "reply": "That's interesting! Can you tell me more about Hello teacher?"
        }

        with testing_session_local() as db:
            messages = list(
                db.scalars(select(ChatMessage).order_by(ChatMessage.id)).all()
            )

        assert [(message.role, message.text) for message in messages] == [
            ("child", "Hello teacher"),
            ("ai", "That's interesting! Can you tell me more about Hello teacher?"),
        ]
        assert all(message.session_id == 1 for message in messages)
    finally:
        app.dependency_overrides.clear()
