from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.session import Base, get_db
from app.main import app
from app.models.chat_message import ChatMessage


@pytest.fixture
def testing_session_local() -> Generator[sessionmaker[Session], None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield testing_session_local


@pytest.fixture
def client(testing_session_local: sessionmaker[Session]) -> Generator[TestClient, None, None]:

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_chat_api_returns_mock_reply_and_stores_messages(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"session_id": 1, "message": "Hello teacher"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "reply": "That's interesting! Can you tell me more about Hello teacher?"
    }

    with testing_session_local() as db:
        messages = list(db.scalars(select(ChatMessage).order_by(ChatMessage.id)).all())

    assert [(message.role, message.text) for message in messages] == [
        ("child", "Hello teacher"),
        ("ai", "That's interesting! Can you tell me more about Hello teacher?"),
    ]
    assert all(message.session_id == 1 for message in messages)


def test_chat_history_returns_messages_in_order(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    with testing_session_local() as db:
        db.add_all(
            [
                ChatMessage(session_id=1, role="child", text="Hello teacher"),
                ChatMessage(
                    session_id=1,
                    role="ai",
                    text="That's interesting! Can you tell me more about Hello teacher?",
                ),
                ChatMessage(session_id=2, role="child", text="Different session"),
            ]
        )
        db.commit()

    response = client.get("/api/v1/chat-history", params={"session_id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == 1
    assert [
        (message["role"], message["text"])
        for message in body["messages"]
    ] == [
        ("child", "Hello teacher"),
        ("ai", "That's interesting! Can you tell me more about Hello teacher?"),
    ]
    assert body["messages"][0]["id"] < body["messages"][1]["id"]
    assert body["messages"][0]["audio_url"] is None
    assert body["messages"][0]["correction"] is None
    assert body["messages"][0]["created_at"] is not None


def test_chat_history_returns_empty_messages_when_session_has_no_records(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/chat-history", params={"session_id": 999})

    assert response.status_code == 200
    assert response.json() == {"session_id": 999, "messages": []}

