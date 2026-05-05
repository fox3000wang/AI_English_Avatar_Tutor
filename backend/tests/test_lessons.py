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
from app.models.lesson import Lesson


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


def test_create_lesson(client: TestClient) -> None:
    response = client.post(
        "/api/v1/lessons",
        json={
            "title": "Animal Talk",
            "topic": "animals",
            "level": "intermediate",
            "scheduled_time": "2026-05-06T19:00:00Z",
            "duration_minutes": 30,
            "created_by_parent_id": 1,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Animal Talk"
    assert body["topic"] == "animals"
    assert body["level"] == "intermediate"
    assert body["scheduled_time"] == "2026-05-06T19:00:00Z"
    assert body["duration_minutes"] == 30
    assert body["created_by_parent_id"] == 1
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_list_lessons_filters_by_parent_and_orders_by_scheduled_time(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    with testing_session_local() as db:
        db.add_all(
            [
                Lesson(
                    title="Later Animal Talk",
                    topic="animals",
                    level="intermediate",
                    scheduled_time=datetime(2026, 5, 7, 19, 0, tzinfo=UTC),
                    duration_minutes=30,
                    created_by_parent_id=1,
                ),
                Lesson(
                    title="Earlier Science Talk",
                    topic="science",
                    level="beginner",
                    scheduled_time=datetime(2026, 5, 6, 19, 0, tzinfo=UTC),
                    duration_minutes=25,
                    created_by_parent_id=1,
                ),
                Lesson(
                    title="Other Parent Lesson",
                    topic="culture",
                    level="beginner",
                    scheduled_time=datetime(2026, 5, 5, 19, 0, tzinfo=UTC),
                    duration_minutes=20,
                    created_by_parent_id=2,
                ),
            ]
        )
        db.commit()

    response = client.get("/api/v1/lessons", params={"created_by_parent_id": 1})

    assert response.status_code == 200
    lessons = response.json()
    assert [lesson["title"] for lesson in lessons] == [
        "Earlier Science Talk",
        "Later Animal Talk",
    ]
    assert all(lesson["created_by_parent_id"] == 1 for lesson in lessons)


def test_list_lessons_returns_empty_list_when_no_lessons(client: TestClient) -> None:
    response = client.get("/api/v1/lessons")

    assert response.status_code == 200
    assert response.json() == []


def test_get_lesson_by_id(client: TestClient, testing_session_local: sessionmaker[Session]) -> None:
    with testing_session_local() as db:
        lesson = Lesson(
            title="Animal Talk",
            topic="animals",
            level="intermediate",
            scheduled_time=datetime(2026, 5, 6, 19, 0, tzinfo=UTC),
            duration_minutes=30,
            created_by_parent_id=1,
        )
        db.add(lesson)
        db.commit()
        lesson_id = lesson.id

    response = client.get(f"/api/v1/lessons/{lesson_id}")

    assert response.status_code == 200
    assert response.json()["id"] == lesson_id
    assert response.json()["title"] == "Animal Talk"


def test_get_lesson_by_id_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/api/v1/lessons/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Lesson not found"}
