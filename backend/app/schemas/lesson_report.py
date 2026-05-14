from pydantic import BaseModel


class LessonReportRequest(BaseModel):
    session_id: int


class LessonReportMistake(BaseModel):
    original: str
    corrected: str
    explanation: str


class LessonReportResponse(BaseModel):
    session_id: int
    summary: str
    strengths: list[str]
    mistakes: list[LessonReportMistake]
    new_words: list[str]
    next_practice: list[str]
