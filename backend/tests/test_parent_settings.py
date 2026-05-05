from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.session import Base, get_db
from app.main import app
from app.models.parent_setting import ParentSetting


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


def test_upsert_parent_setting_creates_setting(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    response = client.put(
        "/api/v1/parent-settings/1",
        json={
            "allowed_topics": ["animals", "science", "history", "culture"],
            "difficulty": "intermediate",
            "daily_minutes": 30,
            "chinese_explanation_allowed": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["child_id"] == 1
    assert body["allowed_topics"] == ["animals", "science", "history", "culture"]
    assert body["difficulty"] == "intermediate"
    assert body["daily_minutes"] == 30
    assert body["chinese_explanation_allowed"] is True
    assert body["created_at"] is not None
    assert body["updated_at"] is not None

    with testing_session_local() as db:
        settings = list(db.scalars(select(ParentSetting)).all())

    assert len(settings) == 1


def test_upsert_parent_setting_updates_existing_setting(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    client.put(
        "/api/v1/parent-settings/1",
        json={
            "allowed_topics": ["animals"],
            "difficulty": "beginner",
            "daily_minutes": 20,
            "chinese_explanation_allowed": False,
        },
    )

    response = client.put(
        "/api/v1/parent-settings/1",
        json={
            "allowed_topics": ["science", "culture"],
            "difficulty": "advanced",
            "daily_minutes": 35,
            "chinese_explanation_allowed": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["child_id"] == 1
    assert body["allowed_topics"] == ["science", "culture"]
    assert body["difficulty"] == "advanced"
    assert body["daily_minutes"] == 35
    assert body["chinese_explanation_allowed"] is True

    with testing_session_local() as db:
        settings = list(db.scalars(select(ParentSetting)).all())

    assert len(settings) == 1


def test_get_parent_setting_returns_setting(
    client: TestClient,
    testing_session_local: sessionmaker[Session],
) -> None:
    with testing_session_local() as db:
        db.add(
            ParentSetting(
                child_id=1,
                allowed_topics=["animals", "history"],
                difficulty="intermediate",
                daily_minutes=30,
                chinese_explanation_allowed=True,
            )
        )
        db.commit()

    response = client.get("/api/v1/parent-settings/1")

    assert response.status_code == 200
    body = response.json()
    assert body["child_id"] == 1
    assert body["allowed_topics"] == ["animals", "history"]
    assert body["difficulty"] == "intermediate"
    assert body["daily_minutes"] == 30
    assert body["chinese_explanation_allowed"] is True


def test_get_parent_setting_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/api/v1/parent-settings/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Parent setting not found"}
