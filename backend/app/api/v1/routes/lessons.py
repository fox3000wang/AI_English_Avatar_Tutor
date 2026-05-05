from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreateRequest, LessonResponse
from app.services.lesson_service import create_lesson, get_lesson, list_lessons

router = APIRouter(prefix="/lessons", tags=["lessons"])


def to_lesson_response(lesson: Lesson) -> LessonResponse:
    return LessonResponse(
        id=lesson.id,
        title=lesson.title,
        topic=lesson.topic,
        level=lesson.level,
        scheduled_time=lesson.scheduled_time,
        duration_minutes=lesson.duration_minutes,
        created_by_parent_id=lesson.created_by_parent_id,
        created_at=lesson.created_at,
        updated_at=lesson.updated_at,
    )


@router.post("", response_model=LessonResponse)
async def create_lesson_endpoint(
    request: LessonCreateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LessonResponse:
    lesson = create_lesson(db=db, lesson_data=request.model_dump())
    return to_lesson_response(lesson)


@router.get("", response_model=list[LessonResponse])
async def list_lessons_endpoint(
    db: Annotated[Session, Depends(get_db)],
    created_by_parent_id: int | None = None,
) -> list[LessonResponse]:
    lessons = list_lessons(db=db, created_by_parent_id=created_by_parent_id)
    return [to_lesson_response(lesson) for lesson in lessons]


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson_endpoint(
    lesson_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> LessonResponse:
    lesson = get_lesson(db=db, lesson_id=lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return to_lesson_response(lesson)
