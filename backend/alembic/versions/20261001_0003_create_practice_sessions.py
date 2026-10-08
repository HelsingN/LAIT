"""Create exercise generations, practice sessions, and attempts.

Attempt.learning_unit_id references learning_units.id with ON DELETE
RESTRICT. A learning-unit delete is blocked while an attempt row points at it.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261001_0003"
down_revision: str | None = "20261001_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "exercise_generations",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lesson_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("accepted_unit_ids", sa.Text(), nullable=False),
        sa.Column("chip_unit_ids", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.CheckConstraint(
            "status in ('completed', 'failed')",
            name="ck_exercise_generations_status",
        ),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_exercise_generations_lesson_id", "exercise_generations", ["lesson_id"])
    op.create_table(
        "exercise_definitions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("generation_id", sa.String(length=64), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("learning_unit_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_type", sa.String(length=64), nullable=False),
        sa.Column("module_package", sa.String(length=128), nullable=False),
        sa.Column("span_start", sa.Integer(), nullable=False),
        sa.Column("span_end", sa.Integer(), nullable=False),
        sa.Column("target_text", sa.Text(), nullable=False),
        sa.Column("sentence", sa.Text(), nullable=False),
        sa.Column("segments", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["generation_id"],
            ["exercise_generations.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_exercise_definitions_generation_id",
        "exercise_definitions",
        ["generation_id"],
    )
    op.create_table(
        "practice_sessions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lesson_id", sa.String(length=64), nullable=False),
        sa.Column("generation_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("cursor", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(
            ["generation_id"],
            ["exercise_generations.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_practice_sessions_lesson_id", "practice_sessions", ["lesson_id"])
    op.create_table(
        "practice_pass_items",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("learning_unit_id", sa.String(length=64), nullable=False),
        sa.Column("definition_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["definition_id"],
            ["exercise_definitions.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["session_id"], ["practice_sessions.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_practice_pass_items_session_id", "practice_pass_items", ["session_id"])
    op.create_table(
        "attempts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("learning_unit_id", sa.String(length=64), nullable=False),
        sa.Column("span_start", sa.Integer(), nullable=False),
        sa.Column("span_end", sa.Integer(), nullable=False),
        sa.Column("unit_text", sa.Text(), nullable=False),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("submitted", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=16), nullable=False),
        sa.Column("expected", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("chunks_used", sa.Text(), nullable=False),
        sa.Column("chunks_missed", sa.Text(), nullable=False),
        sa.Column("natural_alternative", sa.Text(), nullable=True),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["session_id"], ["practice_sessions.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attempts_session_id", "attempts", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_attempts_session_id", table_name="attempts")
    op.drop_table("attempts")
    op.drop_index("ix_practice_pass_items_session_id", table_name="practice_pass_items")
    op.drop_table("practice_pass_items")
    op.drop_index("ix_practice_sessions_lesson_id", table_name="practice_sessions")
    op.drop_table("practice_sessions")
    op.drop_index("ix_exercise_definitions_generation_id", table_name="exercise_definitions")
    op.drop_table("exercise_definitions")
    op.drop_index("ix_exercise_generations_lesson_id", table_name="exercise_generations")
    op.drop_table("exercise_generations")
