"""learning_unit.remove is a logical delete. A removed span can be re-added."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from lait.domain.lesson import Lesson


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'units.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def _lesson(repository, source: str):
    from lait.application.commands.lesson_create import LessonCreate, handle

    return handle(LessonCreate(source=source), repository)


def _row_count(tmp_path: Path) -> int:
    connection = sqlite3.connect(tmp_path / "units.db")
    try:
        row = connection.execute("select count(*) from learning_units").fetchone()
    finally:
        connection.close()
    assert row is not None
    return int(row[0])


class _Lessons:
    def __init__(self, lesson: Lesson) -> None:
        self._lesson = lesson

    def get(self, lesson_id: str) -> Lesson | None:
        if lesson_id == self._lesson.id:
            return self._lesson
        return None


class _Units:
    def __init__(self, frozen: bool) -> None:
        self.frozen = frozen
        self.units: dict[str, object] = {}
        self.writes: list[str] = []

    def has_open_practice_session(self, lesson_id: str) -> bool:
        del lesson_id
        return self.frozen

    def add_unit(self, unit) -> None:
        self.writes.append(f"add:{unit.id}")
        self.units[unit.id] = unit

    def get_unit(self, unit_id: str):
        return self.units.get(unit_id)

    def list_units(self, lesson_id: str):
        return [
            unit
            for unit in self.units.values()
            if unit.lesson_id == lesson_id and unit.removed_at is None
        ]

    def save_unit(self, unit) -> None:
        self.writes.append(f"save:{unit.id}")
        self.units[unit.id] = unit


def _fake_lesson() -> Lesson:
    return Lesson(
        id="lesson-1",
        title="Notes",
        source="ship the queue",
        created_at=datetime(2026, 10, 1, tzinfo=UTC),
    )


def test_remove_sets_removed_at_and_keeps_the_row(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_remove import COMMAND_NAME, LearningUnitRemove
    from lait.application.commands.learning_unit_remove import handle as remove_unit

    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.queries.learning_unit_list import handle as list_units

    source = "alpha beta gamma"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    draft = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=len("alpha")),
        repository,
        repository,
    )
    pending = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=source.index("gamma"), end=len(source)),
        repository,
        repository,
    )
    accepted = accept_unit(
        LearningUnitAccept(lesson_id=lesson.id, unit_id=pending.id),
        repository,
        repository,
    )

    removed_draft = remove_unit(
        LearningUnitRemove(lesson_id=lesson.id, unit_id=draft.id),
        repository,
        repository,
    )
    assert COMMAND_NAME == "learning_unit.remove"
    assert removed_draft.id == draft.id
    assert removed_draft.removed_at is not None
    kept = repository.get_unit(draft.id)
    assert kept is not None
    assert kept.removed_at is not None
    assert kept.text == "alpha"
    listed = list_units(lesson.id, repository)
    assert draft.id not in {unit.id for unit in listed}
    assert accepted.id in {unit.id for unit in listed}
    assert _row_count(tmp_path) == 2

    removed_accepted = remove_unit(
        LearningUnitRemove(lesson_id=lesson.id, unit_id=accepted.id),
        repository,
        repository,
    )
    assert removed_accepted.removed_at is not None
    assert repository.get_unit(accepted.id) is not None
    assert list_units(lesson.id, repository) == []
    assert _row_count(tmp_path) == 2


def test_logical_removed_span_can_be_readded_as_new_unit(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_remove import LearningUnitRemove
    from lait.application.commands.learning_unit_remove import handle as remove_unit

    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.queries.learning_unit_list import handle as list_units

    source = "ship the queue"
    phrase = "the queue"
    start = source.index(phrase)
    end = start + len(phrase)
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=start, end=end),
        repository,
        repository,
    )
    removed = remove_unit(
        LearningUnitRemove(lesson_id=lesson.id, unit_id=created.id),
        repository,
        repository,
    )
    assert removed.removed_at is not None

    again = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=start, end=end),
        repository,
        repository,
    )

    assert again.id != created.id
    assert again.text == created.text == phrase
    assert again.removed_at is None
    kept = repository.get_unit(created.id)
    assert kept is not None
    assert kept.removed_at is not None
    assert kept.text == phrase
    listed = list_units(lesson.id, repository)
    assert [unit.id for unit in listed] == [again.id]
    assert _row_count(tmp_path) == 2


def test_learning_unit_migration_does_not_cascade_deletes() -> None:
    migration = Path("backend/alembic/versions/20261001_0002_create_learning_units.py")
    constraint_lines = [
        line
        for line in migration.read_text(encoding="utf-8").splitlines()
        if "ForeignKeyConstraint" in line or "ondelete" in line
    ]
    text = "\n".join(constraint_lines)
    assert 'ondelete="RESTRICT"' in text
    assert "CASCADE" not in text.upper()


def test_frozen_port_rejects_add_without_row_change() -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.domain.learning_unit import UnitSetFrozenError

    lesson = _fake_lesson()
    units = _Units(frozen=True)
    with pytest.raises(UnitSetFrozenError):
        handle(
            LearningUnitAdd(lesson_id=lesson.id, start=0, end=4),
            _Lessons(lesson),
            units,
        )
    assert units.writes == []
    assert units.units == {}


def test_frozen_port_rejects_remove_without_row_change() -> None:
    from lait.application.commands.learning_unit_remove import LearningUnitRemove, handle

    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.domain.learning_unit import UnitSetFrozenError

    lesson = _fake_lesson()
    units = _Units(frozen=False)
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=4),
        _Lessons(lesson),
        units,
    )
    units.frozen = True
    writes = list(units.writes)
    with pytest.raises(UnitSetFrozenError):
        handle(
            LearningUnitRemove(lesson_id=lesson.id, unit_id=created.id),
            _Lessons(lesson),
            units,
        )
    assert units.writes == writes
    assert units.get_unit(created.id).removed_at is None


def test_frozen_port_rejects_accept_without_row_change() -> None:
    from lait.application.commands.learning_unit_accept import LearningUnitAccept, handle
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.domain.learning_unit import UnitSetFrozenError

    lesson = _fake_lesson()
    units = _Units(frozen=False)
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=4),
        _Lessons(lesson),
        units,
    )
    units.frozen = True
    writes = list(units.writes)
    with pytest.raises(UnitSetFrozenError):
        handle(
            LearningUnitAccept(lesson_id=lesson.id, unit_id=created.id),
            _Lessons(lesson),
            units,
        )
    assert units.writes == writes
    assert units.get_unit(created.id).status == "draft"


def test_not_frozen_port_allows_add(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit

    source = "ship the queue"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    assert repository.has_open_practice_session(lesson.id) is False
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=4),
        repository,
        repository,
    )
    assert created.text == "ship"
    assert created.removed_at is None
