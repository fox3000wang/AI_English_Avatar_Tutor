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
from app.models.lesson_report import LessonReport


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

    with testing_session_local() as db:
        reports = list(db.query(LessonReport).all())

    assert len(reports) == 1
    assert reports[0].session_id == 1
    assert reports[0].summary == body["summary"]
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


def test_latest_lesson_report_returns_most_recent_report(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    with testing_session_local() as db:
        db.add_all(
            [
                LessonReport(
                    session_id=1,
                    summary="Older report",
                    strengths=["Good start"],
                    mistakes=[],
                    new_words=[],
                    next_practice=["Say hello."],
                ),
                LessonReport(
                    session_id=1,
                    summary="Latest report",
                    strengths=["Clear speaking"],
                    mistakes=[],
                    new_words=["favorite"],
                    next_practice=["Use a full sentence."],
                ),
                LessonReport(
                    session_id=2,
                    summary="Other session",
                    strengths=[],
                    mistakes=[],
                    new_words=[],
                    next_practice=[],
                ),
            ]
        )
        db.commit()

    response = client.get("/api/v1/lesson-report/latest", params={"session_id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == 1
    assert body["summary"] == "Latest report"
    assert body["new_words"] == ["favorite"]


def test_latest_lesson_report_returns_null_when_missing(client: TestClient) -> None:
    response = client.get("/api/v1/lesson-report/latest", params={"session_id": 999})

    assert response.status_code == 200
    assert response.json() is None
