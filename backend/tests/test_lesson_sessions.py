from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.session import Base, get_db
from app.main import app
from app.models.lesson_session import LessonSession


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


def test_create_lesson_session(client: TestClient) -> None:
    response = client.post(
        "/api/v1/lesson-sessions",
        json={"lesson_id": 1, "child_id": 1},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["lesson_id"] == 1
    assert body["child_id"] == 1
    assert body["started_at"] is not None
    assert body["ended_at"] is None
    assert body["summary"] is None
    assert body["score"] is None


def test_end_lesson_session(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    with testing_session_local() as db:
        lesson_session = LessonSession(
            lesson_id=1,
            child_id=1,
            started_at=datetime.now(UTC),
        )
        db.add(lesson_session)
        db.commit()
        session_id = lesson_session.id

    response = client.post(
        f"/api/v1/lesson-sessions/{session_id}/end",
        json={"summary": "Today we practiced animal topics.", "score": 85},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == session_id
    assert body["lesson_id"] == 1
    assert body["child_id"] == 1
    assert body["ended_at"] is not None
    assert body["summary"] == "Today we practiced animal topics."
    assert body["score"] == 85


def test_end_lesson_session_returns_404_when_missing(client: TestClient) -> None:
    response = client.post(
        "/api/v1/lesson-sessions/999/end",
        json={"summary": "Today we practiced animal topics.", "score": 85},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Lesson session not found"}
