from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
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


def test_lesson_report_returns_mock_report_from_chat_history(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    with testing_session_local() as db:
        db.add_all(
            [
                ChatMessage(session_id=1, role="child", text="Hello teacher"),
                ChatMessage(session_id=1, role="ai", text="Hello! How are you today?"),
            ]
        )
        db.commit()

    response = client.post("/api/v1/lesson-report", json={"session_id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == 1
    assert body["summary"]
    assert body["strengths"]
    assert body["mistakes"][0]["corrected"] == "I like cats."
    assert body["new_words"]
    assert body["next_practice"]
    get_settings.cache_clear()


def test_lesson_report_returns_friendly_empty_report(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    response = client.post("/api/v1/lesson-report", json={"session_id": 999})

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == 999
    assert "not much class conversation" in body["summary"]
    assert body["mistakes"] == []
    get_settings.cache_clear()
