from datetime import datetime

from pydantic import BaseModel


class ParentSettingUpsertRequest(BaseModel):
    allowed_topics: list[str]
    difficulty: str
    daily_minutes: int
    chinese_explanation_allowed: bool


class ParentSettingResponse(BaseModel):
    id: int
    child_id: int
    allowed_topics: list[str]
    difficulty: str
    daily_minutes: int
    chinese_explanation_allowed: bool
    created_at: datetime
    updated_at: datetime
