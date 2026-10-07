"""exercise.submit_attempt stores a durable Attempt and leaves the session open."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'submit.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url), database_url


def _registry():
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    return validate_catalog(load_bundled_catalog())


def _ready_session(tmp_path: Path):
    from lait.application.commands.exercise_generate import ExerciseGenerate
    from lait.application.commands.exercise_generate import handle as generate
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.lesson_create import LessonCreate
    from lait.application.commands.lesson_create import handle as create_lesson
    from lait.application.commands.practice_start import PracticeStart
    from lait.application.commands.practice_start import handle as start

    source = "I was responsible for rolling out the migration."
    text = "rolling out"
    repository, database_url = _repository(tmp_path)
    lesson = create_lesson(LessonCreate(source=source), repository)
    start_at = source.index(text)
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=start_at, end=start_at + len(text)),
        repository,
        repository,
    )
    unit = accept_unit(
        LearningUnitAccept(lesson_id=lesson.id, unit_id=created.id),
        repository,
        repository,
    )
    registry = _registry()
    generate(ExerciseGenerate(lesson_id=lesson.id), repository, repository, registry)
    session = start(PracticeStart(lesson_id=lesson.id), repository, repository, registry)
    return repository, database_url, lesson, unit, session


def test_submit_stores_attempt_feedback_and_advances_while_session_stays_open(
    tmp_path: Path,
) -> None:
    from lait.application.commands.exercise_submit_attempt import (
        COMMAND_NAME,
        SubmitAttempt,
        handle,
    )
    from lait.application.queries.practice_get import handle as current_item

    repository, _database_url, _lesson, unit, session = _ready_session(tmp_path)
    result = handle(
        SubmitAttempt(session_id=session.session_id, kind="typed", text="Rolling out"),
        repository,
        _registry(),
    )
    view = current_item(session.session_id, repository)

    assert COMMAND_NAME == "exercise.submit_attempt"
    assert result.session_open is True
    assert result.cursor == 1
    assert result.category == "correct"
    assert result.expected == "rolling out"
    assert result.explanation == "The response matches the target for this exercise."
    assert result.natural_alternative is None
    assert result.chunks_used == ("rolling out",)
    assert result.chunks_missed == ()
    assert result.learning_unit_id == unit.id
    assert result.span_start == unit.start
    assert result.span_end == unit.end
    assert result.unit_text == unit.text
    assert view.open is True
    assert view.current is None
    assert repository.has_open_practice_session(_lesson.id) is True


def test_same_item_accepted_twice_creates_two_attempts(tmp_path: Path) -> None:
    from lait.application.commands.exercise_submit_attempt import SubmitAttempt, handle

    repository, database_url, _lesson, unit, session = _ready_session(tmp_path)
    handle(
        SubmitAttempt(session_id=session.session_id, kind="typed", text="Rolling out"),
        repository,
        _registry(),
    )
    second = handle(
        SubmitAttempt(
            session_id=session.session_id,
            kind="typed",
            text="nope",
            target_learning_unit_id=unit.id,
        ),
        repository,
        _registry(),
    )

    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        rows = list(
            connection.execute(
                "select learning_unit_id, unit_text, span_start, span_end from attempts "
                "order by created_at, id"
            )
        )
    finally:
        connection.close()
    assert len(rows) == 2
    assert rows[0][0] == rows[1][0] == unit.id
    assert rows[0][1] == rows[1][1] == "rolling out"
    assert rows[0][2] == rows[1][2] == unit.start
    assert rows[0][3] == rows[1][3] == unit.end
    assert second.session_open is True
    assert second.category == "incorrect"
    assert repository.has_open_practice_session(_lesson.id) is True


def test_attempt_unit_fk_is_on_delete_restrict_and_copies_span_and_text(tmp_path: Path) -> None:
    from lait.application.commands.exercise_submit_attempt import SubmitAttempt, handle

    repository, database_url, _lesson, unit, session = _ready_session(tmp_path)
    handle(
        SubmitAttempt(session_id=session.session_id, kind="typed", text="Rolling out"),
        repository,
        _registry(),
    )
    migration = Path("backend/alembic/versions/20261001_0003_create_practice_sessions.py")
    text = migration.read_text(encoding="utf-8")
    assert 'ondelete="RESTRICT"' in text
    assert "CASCADE" not in text.upper()
    assert "learning_units.id" in text

    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        connection.execute("PRAGMA foreign_keys=ON")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("delete from learning_units where id = ?", (unit.id,))
        copied = connection.execute(
            "select learning_unit_id, span_start, span_end, unit_text from attempts"
        ).fetchone()
    finally:
        connection.close()
    assert copied == (unit.id, unit.start, unit.end, unit.text)
