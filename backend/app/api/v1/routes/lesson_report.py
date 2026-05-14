from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lesson_report import LessonReportRequest, LessonReportResponse
from app.services.lesson_report_service import create_lesson_report

router = APIRouter(tags=["lesson-report"])


@router.post("/lesson-report", response_model=LessonReportResponse)
async def lesson_report(
    request: LessonReportRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LessonReportResponse:
    return create_lesson_report(db=db, session_id=request.session_id)
