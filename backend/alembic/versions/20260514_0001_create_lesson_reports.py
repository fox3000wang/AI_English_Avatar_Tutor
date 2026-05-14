"""create lesson reports table

Revision ID: 20260514_0001
Revises: 5e91d75536e6
Create Date: 2026-05-14 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260514_0001"
down_revision: str | None = "5e91d75536e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lesson_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("mistakes", sa.JSON(), nullable=False),
        sa.Column("new_words", sa.JSON(), nullable=False),
        sa.Column("next_practice", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["session_id"], ["lesson_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lesson_reports_id"), "lesson_reports", ["id"], unique=False)
    op.create_index(
        op.f("ix_lesson_reports_session_id"),
        "lesson_reports",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_lesson_reports_session_id"), table_name="lesson_reports")
    op.drop_index(op.f("ix_lesson_reports_id"), table_name="lesson_reports")
    op.drop_table("lesson_reports")
