from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lesson import Lesson


def create_lesson(db: Session, lesson_data: dict) -> Lesson:
    lesson = Lesson(**lesson_data)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson


def list_lessons(db: Session, created_by_parent_id: int | None = None) -> list[Lesson]:
    statement = select(Lesson)
    if created_by_parent_id is not None:
        statement = statement.where(Lesson.created_by_parent_id == created_by_parent_id)

    return list(db.scalars(statement.order_by(Lesson.scheduled_time)).all())


def get_lesson(db: Session, lesson_id: int) -> Lesson | None:
    return db.get(Lesson, lesson_id)
