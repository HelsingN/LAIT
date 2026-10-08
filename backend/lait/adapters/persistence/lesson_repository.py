"""SQLite lesson repository. Ordering is created_at descending, then id ascending."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from lait.adapters.persistence.models import LessonRow
from lait.domain.lesson import Lesson


def _to_lesson(row: LessonRow) -> Lesson:
    return Lesson(
        id=row.id,
        title=row.title,
        source=row.source,
        created_at=datetime.fromisoformat(row.created_at),
    )


class SqlAlchemyLessonRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def add(self, lesson: Lesson) -> None:
        row = LessonRow(
            id=lesson.id,
            title=lesson.title,
            source=lesson.source,
            created_at=lesson.created_at.isoformat(),
        )
        with self._session_factory() as session:
            session.add(row)
            session.commit()

    def get(self, lesson_id: str) -> Lesson | None:
        with self._session_factory() as session:
            row = session.get(LessonRow, lesson_id)
            if row is None:
                return None
            return _to_lesson(row)

    def list_lessons(self) -> list[Lesson]:
        statement = select(LessonRow).order_by(LessonRow.created_at.desc(), LessonRow.id.asc())
        with self._session_factory() as session:
            rows = session.scalars(statement).all()
            return [_to_lesson(row) for row in rows]
