"""One open practice session per lesson.

Partial unique index uq_practice_sessions_one_open_per_lesson rejects a
second row with status open for the same lesson. Closed and abandoned
rows stay non-unique under ix_practice_sessions_lesson_id.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261002_0004"
down_revision: str | None = "20261001_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "uq_practice_sessions_one_open_per_lesson",
        "practice_sessions",
        ["lesson_id"],
        unique=True,
        sqlite_where=sa.text("status = 'open'"),
        postgresql_where=sa.text("status = 'open'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_practice_sessions_one_open_per_lesson",
        table_name="practice_sessions",
    )
