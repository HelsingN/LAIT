"""practice.finish returns to the workspace. practice.start_over keeps Attempts."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'finish.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url), database_url


def _registry():
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    return validate_catalog(load_bundled_catalog())


def _ready_session(tmp_path: Path):
    from lait.application.commands.exercise_generate import ExerciseGenerate
    from lait.application.commands.exercise_generate import handle as generate
    from lait.application.commands.exercise_submit_attempt import SubmitAttempt
    from lait.application.commands.exercise_submit_attempt import handle as submit_attempt
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
    submit_attempt(
        SubmitAttempt(session_id=session.session_id, kind="typed", text="Rolling out"),
        repository,
        registry,
    )
    return repository, database_url, lesson, unit, session, source


def _attempt_rows(database_url: str) -> list[tuple[str, str]]:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        return list(connection.execute("select id, unit_text from attempts order by id"))
    finally:
        connection.close()


def _session_statuses(database_url: str) -> dict[str, str]:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        rows = connection.execute("select id, status from practice_sessions").fetchall()
    finally:
        connection.close()
    return {session_id: status for session_id, status in rows}


def test_finish_closes_session_and_unfreezes_units(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.practice_finish import COMMAND_NAME, PracticeFinish, handle
    from lait.application.queries.practice_get import handle as current_item
    from lait.domain.learning_unit import DRAFT

    repository, database_url, lesson, _unit, session, source = _ready_session(tmp_path)
    attempts_before = _attempt_rows(database_url)
    closed = handle(PracticeFinish(session_id=session.session_id), repository)
    viewed = current_item(session.session_id, repository)
    added_text = "migration"
    added_at = source.index(added_text)
    added = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=added_at, end=added_at + len(added_text)),
        repository,
        repository,
    )

    assert COMMAND_NAME == "practice.finish"
    assert closed.session_id == session.session_id
    assert closed.lesson_id == lesson.id
    assert closed.open is False
    assert closed.current is None
    assert viewed.open is False
    assert viewed.current is None
    assert repository.has_open_practice_session(lesson.id) is False
    assert _session_statuses(database_url) == {session.session_id: "closed"}
    assert _attempt_rows(database_url) == attempts_before
    assert added.status == DRAFT
    assert added.text == added_text


def test_start_over_keeps_attempts_and_leaves_units_frozen(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.practice_start_over import (
        COMMAND_NAME,
        PracticeStartOver,
        handle,
    )
    from lait.domain.learning_unit import UnitSetFrozenError

    repository, database_url, lesson, unit, session, source = _ready_session(tmp_path)
    attempts_before = _attempt_rows(database_url)
    restarted = handle(
        PracticeStartOver(session_id=session.session_id),
        repository,
        repository,
        _registry(),
    )
    added_text = "migration"
    added_at = source.index(added_text)

    assert COMMAND_NAME == "practice.start_over"
    assert restarted.session_id != session.session_id
    assert restarted.lesson_id == lesson.id
    assert restarted.open is True
    assert restarted.cursor == 0
    assert restarted.current is not None
    assert restarted.current.mode == "typed"
    assert restarted.current.learning_unit_id == unit.id
    assert repository.has_open_practice_session(lesson.id) is True
    statuses = _session_statuses(database_url)
    assert statuses[session.session_id] == "abandoned"
    assert statuses[restarted.session_id] == "open"
    assert len(statuses) == 2
    assert _attempt_rows(database_url) == attempts_before
    assert len(attempts_before) == 1
    with pytest.raises(UnitSetFrozenError):
        add_unit(
            LearningUnitAdd(lesson_id=lesson.id, start=added_at, end=added_at + len(added_text)),
            repository,
            repository,
        )
