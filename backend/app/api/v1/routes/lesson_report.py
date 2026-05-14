from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lesson_report import LessonReportRequest, LessonReportResponse
from app.services.lesson_report_service import create_lesson_report, get_latest_lesson_report

router = APIRouter(tags=["lesson-report"])


@router.post("/lesson-report", response_model=LessonReportResponse)
async def lesson_report(
    request: LessonReportRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LessonReportResponse:
    return create_lesson_report(db=db, session_id=request.session_id)


@router.get("/lesson-report/latest", response_model=LessonReportResponse | None)
async def latest_lesson_report(
    session_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> LessonReportResponse | None:
    return get_latest_lesson_report(db=db, session_id=session_id)
