from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.lesson_session import LessonSession


def create_lesson_session(db: Session, lesson_id: int, child_id: int) -> LessonSession:
    lesson_session = LessonSession(
        lesson_id=lesson_id,
        child_id=child_id,
        started_at=datetime.now(UTC),
    )
    db.add(lesson_session)
    db.commit()
    db.refresh(lesson_session)

    return lesson_session


def end_lesson_session(
    db: Session,
    session_id: int,
    summary: str | None,
    score: int | None,
) -> LessonSession | None:
    lesson_session = db.get(LessonSession, session_id)
    if lesson_session is None:
        return None

    lesson_session.ended_at = datetime.now(UTC)
    lesson_session.summary = summary
    lesson_session.score = score
    db.commit()
    db.refresh(lesson_session)

    return lesson_session
