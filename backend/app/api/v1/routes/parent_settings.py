from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.parent_setting import ParentSetting
from app.schemas.parent_setting import ParentSettingResponse, ParentSettingUpsertRequest
from app.services.parent_setting_service import get_parent_setting, upsert_parent_setting

router = APIRouter(prefix="/parent-settings", tags=["parent-settings"])


def to_parent_setting_response(parent_setting: ParentSetting) -> ParentSettingResponse:
    return ParentSettingResponse(
        id=parent_setting.id,
        child_id=parent_setting.child_id,
        allowed_topics=parent_setting.allowed_topics,
        difficulty=parent_setting.difficulty,
        daily_minutes=parent_setting.daily_minutes,
        chinese_explanation_allowed=parent_setting.chinese_explanation_allowed,
        created_at=parent_setting.created_at,
        updated_at=parent_setting.updated_at,
    )


@router.put("/{child_id}", response_model=ParentSettingResponse)
async def upsert_child_setting(
    child_id: int,
    request: ParentSettingUpsertRequest,
    db: Annotated[Session, Depends(get_db)],
) -> ParentSettingResponse:
    parent_setting = upsert_parent_setting(
        db=db,
        child_id=child_id,
        setting_data=request.model_dump(),
    )
    return to_parent_setting_response(parent_setting)


@router.get("/{child_id}", response_model=ParentSettingResponse)
async def get_child_setting(
    child_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> ParentSettingResponse:
    parent_setting = get_parent_setting(db=db, child_id=child_id)
    if parent_setting is None:
        raise HTTPException(status_code=404, detail="Parent setting not found")

    return to_parent_setting_response(parent_setting)
