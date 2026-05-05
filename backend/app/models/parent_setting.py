from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ParentSetting(Base):
    __tablename__ = "parent_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    allowed_topics: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    daily_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    chinese_explanation_allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    child = relationship("User", foreign_keys=[child_id])
