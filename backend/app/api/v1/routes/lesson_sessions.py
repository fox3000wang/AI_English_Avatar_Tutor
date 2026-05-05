from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lesson_session import (
    LessonSessionCreateRequest,
    LessonSessionEndRequest,
    LessonSessionResponse,
)
from app.services.lesson_session_service import create_lesson_session, end_lesson_session

router = APIRouter(prefix="/lesson-sessions", tags=["lesson-sessions"])


@router.post("", response_model=LessonSessionResponse)
async def create_session(
    request: LessonSessionCreateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LessonSessionResponse:
    lesson_session = create_lesson_session(
        db=db,
        lesson_id=request.lesson_id,
        child_id=request.child_id,
    )
    return LessonSessionResponse(
        id=lesson_session.id,
        lesson_id=lesson_session.lesson_id,
        child_id=lesson_session.child_id,
        started_at=lesson_session.started_at,
        ended_at=lesson_session.ended_at,
        summary=lesson_session.summary,
        score=lesson_session.score,
    )


@router.post("/{session_id}/end", response_model=LessonSessionResponse)
async def end_session(
    session_id: int,
    request: LessonSessionEndRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LessonSessionResponse:
    lesson_session = end_lesson_session(
        db=db,
        session_id=session_id,
        summary=request.summary,
        score=request.score,
    )
    if lesson_session is None:
        raise HTTPException(status_code=404, detail="Lesson session not found")

    return LessonSessionResponse(
        id=lesson_session.id,
        lesson_id=lesson_session.lesson_id,
        child_id=lesson_session.child_id,
        started_at=lesson_session.started_at,
        ended_at=lesson_session.ended_at,
        summary=lesson_session.summary,
        score=lesson_session.score,
    )
