from datetime import UTC, datetime

from pydantic import BaseModel, field_serializer


class LessonCreateRequest(BaseModel):
    title: str
    topic: str
    level: str
    scheduled_time: datetime
    duration_minutes: int
    created_by_parent_id: int


class LessonResponse(BaseModel):
    id: int
    title: str
    topic: str
    level: str
    scheduled_time: datetime
    duration_minutes: int
    created_by_parent_id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("scheduled_time", "created_at", "updated_at")
    def serialize_datetime(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
