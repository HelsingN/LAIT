"""Create the lessons table."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261001_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lessons",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_lessons_created_at", "lessons", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_lessons_created_at", table_name="lessons")
    op.drop_table("lessons")
