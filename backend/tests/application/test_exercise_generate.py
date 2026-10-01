"""exercise.generate persists a terminal status for accepted units only."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'generate.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def _registry():
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    return validate_catalog(load_bundled_catalog())


def _lesson(repository, source: str):
    from lait.application.commands.lesson_create import LessonCreate, handle

    return handle(LessonCreate(source=source), repository)


def _accept(repository, lesson_id: str, source: str, text: str):
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit

    start = source.index(text)
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson_id, start=start, end=start + len(text)),
        repository,
        repository,
    )
    return accept_unit(
        LearningUnitAccept(lesson_id=lesson_id, unit_id=created.id),
        repository,
        repository,
    )


def _rows(tmp_path: Path, sql: str) -> list[tuple]:
    connection = sqlite3.connect(tmp_path / "generate.db")
    try:
        return list(connection.execute(sql))
    finally:
        connection.close()


def test_generate_with_accepted_units_stores_completed_and_matching_count(tmp_path: Path) -> None:
    from lait.application.commands.exercise_generate import COMMAND_NAME, ExerciseGenerate, handle

    source = "I was responsible for rolling out the migration."
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    unit = _accept(repository, lesson.id, source, "rolling out")

    outcome = handle(
        ExerciseGenerate(lesson_id=lesson.id),
        repository,
        repository,
        _registry(),
    )

    command_source = Path("backend/lait/application/commands/exercise_generate.py").read_text(
        encoding="utf-8"
    )
    lowered = command_source.lower()
    assert COMMAND_NAME == "exercise.generate"
    assert "backgroundtasks" not in lowered
    assert "celery" not in lowered
    assert "redis" not in lowered
    assert "queued" not in lowered
    assert "running" not in lowered
    assert outcome.status == "completed"
    assert outcome.definition_count == 1
    assert set(outcome.accepted_unit_ids) == {unit.id}
    stored = _rows(tmp_path, "select status, accepted_unit_ids from exercise_generations")
    assert len(stored) == 1
    assert stored[0][0] == "completed"
    assert set(json.loads(stored[0][1])) == {unit.id}
    assert _rows(tmp_path, "select count(*) from exercise_definitions")[0][0] == 1
    assert _rows(tmp_path, "select learning_unit_id from exercise_definitions")[0][0] == unit.id


def test_generate_with_zero_accepted_stores_failed_and_zero_definitions(tmp_path: Path) -> None:
    from lait.application.commands.exercise_generate import ExerciseGenerate, handle

    source = "I was responsible for rolling out the migration."
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    outcome = handle(
        ExerciseGenerate(lesson_id=lesson.id),
        repository,
        repository,
        _registry(),
    )

    assert outcome.status == "failed"
    assert outcome.definition_count == 0
    assert outcome.accepted_unit_ids == ()
    stored = _rows(tmp_path, "select status, accepted_unit_ids from exercise_generations")
    assert stored == [("failed", "[]")]
    assert _rows(tmp_path, "select count(*) from exercise_definitions")[0][0] == 0


def test_generate_skips_drafts_and_persists_only_terminal_status(tmp_path: Path) -> None:
    from lait.application.commands.exercise_generate import ExerciseGenerate, handle
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit

    source = "alpha beta gamma"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    accepted = _accept(repository, lesson.id, source, "alpha")
    draft_start = source.index("gamma")
    add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=draft_start, end=draft_start + len("gamma")),
        repository,
        repository,
    )

    outcome = handle(
        ExerciseGenerate(lesson_id=lesson.id),
        repository,
        repository,
        _registry(),
    )

    assert outcome.status == "completed"
    assert outcome.definition_count == 1
    assert set(outcome.accepted_unit_ids) == {accepted.id}
    statuses = {row[0] for row in _rows(tmp_path, "select status from exercise_generations")}
    assert statuses <= {"completed", "failed"}
    unit_ids = [row[0] for row in _rows(tmp_path, "select learning_unit_id from exercise_definitions")]
    assert unit_ids == [accepted.id]


def test_generate_unknown_lesson_writes_nothing(tmp_path: Path) -> None:
    from lait.application.commands.exercise_generate import ExerciseGenerate, handle
    from lait.application.queries.lesson_get import LessonNotFoundError

    repository = _repository(tmp_path)
    with pytest.raises(LessonNotFoundError):
        handle(ExerciseGenerate(lesson_id="missing"), repository, repository, _registry())
    assert _rows(tmp_path, "select count(*) from exercise_generations")[0][0] == 0
