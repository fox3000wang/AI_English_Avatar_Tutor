from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.core.config import get_settings
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


def test_voice_chat_returns_texts_audio_url_and_stores_ai_audio_url(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    response = client.post(
        "/api/v1/voice-chat",
        data={"session_id": "1"},
        files={"file": ("hello.wav", b"fake audio bytes", "audio/wav")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_text"] == "Hello teacher"
    assert body["ai_text"] == "That's interesting! Can you tell me more about Hello teacher?"
    assert body["audio_url"].startswith("/storage/audio/")
    assert body["audio_url"].endswith(".mp3")

    with testing_session_local() as db:
        messages = list(db.scalars(select(ChatMessage).order_by(ChatMessage.id)).all())

    assert [(message.role, message.text) for message in messages] == [
        ("child", "Hello teacher"),
        ("ai", "That's interesting! Can you tell me more about Hello teacher?"),
    ]
    assert messages[0].audio_url is None
    assert messages[1].audio_url == body["audio_url"]
    assert all(message.session_id == 1 for message in messages)

    audio_path = Path("storage/audio") / Path(body["audio_url"]).name
    assert audio_path.exists()
    get_settings.cache_clear()


def test_voice_chat_returns_400_when_file_is_missing(client: TestClient) -> None:
    response = client.post("/api/v1/voice-chat", data={"session_id": "1"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Audio file is required"}


def test_voice_chat_returns_422_when_session_id_is_missing(client: TestClient) -> None:
    response = client.post(
        "/api/v1/voice-chat",
        files={"file": ("hello.wav", b"fake audio bytes", "audio/wav")},
    )

    assert response.status_code == 422
