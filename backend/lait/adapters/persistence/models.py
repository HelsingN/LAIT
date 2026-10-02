"""SQLite tables owned by the persistence adapter."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class LessonRow(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, index=True)


class LearningUnitRow(Base):
    """Span offsets are Unicode code points (Python str indices), not UTF-16."""

    __tablename__ = "learning_units"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lesson_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("lessons.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    span_start: Mapped[int] = mapped_column(Integer, nullable=False)
    span_end: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    removed_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False)


class ExerciseGenerationRow(Base):
    __tablename__ = "exercise_generations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lesson_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("lessons.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    accepted_unit_ids: Mapped[str] = mapped_column(Text, nullable=False)
    chip_unit_ids: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False)


class ExerciseDefinitionRow(Base):
    __tablename__ = "exercise_definitions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    generation_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("exercise_generations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    learning_unit_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("learning_units.id", ondelete="RESTRICT"),
        nullable=False,
    )
    exercise_type: Mapped[str] = mapped_column(String(64), nullable=False)
    module_package: Mapped[str] = mapped_column(String(128), nullable=False)
    span_start: Mapped[int] = mapped_column(Integer, nullable=False)
    span_end: Mapped[int] = mapped_column(Integer, nullable=False)
    target_text: Mapped[str] = mapped_column(Text, nullable=False)
    sentence: Mapped[str] = mapped_column(Text, nullable=False)
    segments: Mapped[str] = mapped_column(Text, nullable=False)


class PracticeSessionRow(Base):
    __tablename__ = "practice_sessions"
    __table_args__ = (
        Index(
            "uq_practice_sessions_one_open_per_lesson",
            "lesson_id",
            unique=True,
            sqlite_where=text("status = 'open'"),
            postgresql_where=text("status = 'open'"),
        ),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lesson_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("lessons.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    generation_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("exercise_generations.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    cursor: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False)


class PracticePassItemRow(Base):
    __tablename__ = "practice_pass_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("practice_sessions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    learning_unit_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("learning_units.id", ondelete="RESTRICT"),
        nullable=False,
    )
    definition_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("exercise_definitions.id", ondelete="RESTRICT"),
        nullable=False,
    )


class AttemptRow(Base):
    """Unit id, code-point span, and unit text are copied at submit."""

    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("practice_sessions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    learning_unit_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("learning_units.id", ondelete="RESTRICT"),
        nullable=False,
    )
    span_start: Mapped[int] = mapped_column(Integer, nullable=False)
    span_end: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_text: Mapped[str] = mapped_column(Text, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    submitted: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(16), nullable=False)
    expected: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    chunks_used: Mapped[str] = mapped_column(Text, nullable=False)
    chunks_missed: Mapped[str] = mapped_column(Text, nullable=False)
    natural_alternative: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False)
