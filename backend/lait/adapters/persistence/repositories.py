"""SQLite learning-unit repository. Live rows are those with removed_at unset."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from lait.adapters.persistence.lesson_repository import SqlAlchemyLessonRepository
from lait.adapters.persistence.models import LearningUnitRow
from lait.domain.learning_unit import LearningUnit, LearningUnitNotFoundError
from lait.domain.lesson import Lesson


def _to_unit(row: LearningUnitRow) -> LearningUnit:
    return LearningUnit(
        id=row.id,
        lesson_id=row.lesson_id,
        start=row.span_start,
        end=row.span_end,
        text=row.text,
        status=row.status,
        created_at=datetime.fromisoformat(row.created_at),
        removed_at=None if row.removed_at is None else datetime.fromisoformat(row.removed_at),
    )


class SqlAlchemyLearningUnitRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def add_unit(self, unit: LearningUnit) -> None:
        row = LearningUnitRow(
            id=unit.id,
            lesson_id=unit.lesson_id,
            span_start=unit.start,
            span_end=unit.end,
            text=unit.text,
            status=unit.status,
            removed_at=None if unit.removed_at is None else unit.removed_at.isoformat(),
            created_at=unit.created_at.isoformat(),
        )
        with self._session_factory() as session:
            session.add(row)
            session.commit()

    def get_unit(self, unit_id: str) -> LearningUnit | None:
        with self._session_factory() as session:
            row = session.get(LearningUnitRow, unit_id)
            if row is None:
                return None
            return _to_unit(row)

    def list_units(self, lesson_id: str) -> list[LearningUnit]:
        statement = (
            select(LearningUnitRow)
            .where(
                LearningUnitRow.lesson_id == lesson_id,
                LearningUnitRow.removed_at.is_(None),
            )
            .order_by(LearningUnitRow.span_start.asc(), LearningUnitRow.id.asc())
        )
        with self._session_factory() as session:
            rows = session.scalars(statement).all()
            return [_to_unit(row) for row in rows]

    def save_unit(self, unit: LearningUnit) -> None:
        with self._session_factory() as session:
            row = session.get(LearningUnitRow, unit.id)
            if row is None:
                raise LearningUnitNotFoundError(unit.id)
            row.status = unit.status
            row.removed_at = None if unit.removed_at is None else unit.removed_at.isoformat()
            session.commit()

    def has_open_practice_session(self, lesson_id: str) -> bool:
        """Plan 01-05 replaces this body. No PracticeSession table exists yet."""
        del lesson_id
        return False


class RepositoryBundle:
    """Lesson and learning-unit ports over one session factory.

    create_app already stores the object from open_repository. Unit commands
    use that same object so app.py stays untouched.
    """

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._lessons = SqlAlchemyLessonRepository(session_factory)
        self._units = SqlAlchemyLearningUnitRepository(session_factory)

    def add(self, lesson: Lesson) -> None:
        self._lessons.add(lesson)

    def get(self, lesson_id: str) -> Lesson | None:
        return self._lessons.get(lesson_id)

    def list_lessons(self) -> list[Lesson]:
        return self._lessons.list_lessons()

    def add_unit(self, unit: LearningUnit) -> None:
        self._units.add_unit(unit)

    def get_unit(self, unit_id: str) -> LearningUnit | None:
        return self._units.get_unit(unit_id)

    def list_units(self, lesson_id: str) -> list[LearningUnit]:
        return self._units.list_units(lesson_id)

    def save_unit(self, unit: LearningUnit) -> None:
        self._units.save_unit(unit)

    def has_open_practice_session(self, lesson_id: str) -> bool:
        return self._units.has_open_practice_session(lesson_id)
