from datetime import datetime

from pydantic import BaseModel


class LessonSessionCreateRequest(BaseModel):
    lesson_id: int
    child_id: int


class LessonSessionEndRequest(BaseModel):
    summary: str | None = None
    score: int | None = None


class LessonSessionResponse(BaseModel):
    id: int
    lesson_id: int
    child_id: int
    started_at: datetime
    ended_at: datetime | None
    summary: str | None
    score: int | None
