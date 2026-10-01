"""Create the learning_units table.

Span offsets are Unicode code points (Python str indices), not DOM UTF-16
offsets. Attempt.learning_unit_id will reference this id with ON DELETE
RESTRICT. This revision does not create ON DELETE CASCADE.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261001_0002"
down_revision: str | None = "20261001_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "learning_units",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lesson_id", sa.String(length=64), nullable=False),
        sa.Column("span_start", sa.Integer(), nullable=False),
        sa.Column("span_end", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("removed_at", sa.String(length=40), nullable=True),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_learning_units_lesson_id", "learning_units", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_learning_units_lesson_id", table_name="learning_units")
    op.drop_table("learning_units")
