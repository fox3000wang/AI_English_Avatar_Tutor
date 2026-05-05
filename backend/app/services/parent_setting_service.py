from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.parent_setting import ParentSetting


def get_parent_setting(db: Session, child_id: int) -> ParentSetting | None:
    return db.scalar(select(ParentSetting).where(ParentSetting.child_id == child_id))


def upsert_parent_setting(
    db: Session,
    child_id: int,
    setting_data: dict,
) -> ParentSetting:
    parent_setting = get_parent_setting(db=db, child_id=child_id)

    if parent_setting is None:
        parent_setting = ParentSetting(child_id=child_id, **setting_data)
        db.add(parent_setting)
    else:
        for key, value in setting_data.items():
            setattr(parent_setting, key, value)

    db.commit()
    db.refresh(parent_setting)

    return parent_setting
