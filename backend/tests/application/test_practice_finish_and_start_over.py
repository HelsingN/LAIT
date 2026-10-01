"""practice.finish returns to the workspace. practice.start_over keeps Attempts."""

from __future__ import annotations

import inspect
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


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


def test_http_finish_and_start_over_only_map_dtos(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate

    database_url = f"sqlite:///{(tmp_path / 'http-finish.db').as_posix()}"
    migrate(database_url)
    client = TestClient(create_app(database_url))
    source = "I was responsible for rolling out the migration."
    text = "rolling out"
    start_at = source.index(text)
    created = client.post("/api/lessons", json={"source": source})
    assert created.status_code == 201
    lesson_id = created.json()["id"]
    unit = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": start_at, "end": start_at + len(text)},
    )
    assert unit.status_code == 201
    accepted = client.post(f"/api/lessons/{lesson_id}/learning-units/{unit.json()['id']}/accept")
    assert accepted.status_code == 200
    generated = client.post(f"/api/lessons/{lesson_id}/exercises/generate")
    assert generated.status_code == 200
    started = client.post("/api/practice-sessions", json={"lesson_id": lesson_id})
    assert started.status_code == 201
    session_id = started.json()["session_id"]
    submitted = client.post(
        f"/api/practice-sessions/{session_id}/attempts",
        json={"kind": "typed", "text": "Rolling out"},
    )
    assert submitted.status_code == 200
    attempts_before = _attempt_rows(database_url)

    restarted = client.post(f"/api/practice-sessions/{session_id}/start-over")
    assert restarted.status_code == 200
    restarted_body = restarted.json()
    assert restarted_body["open"] is True
    assert restarted_body["session_id"] != session_id
    assert restarted_body["cursor"] == 0
    assert restarted_body["current"]["mode"] == "typed"
    migration_at = source.index("migration")
    blocked = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": migration_at, "end": migration_at + len("migration")},
    )
    assert blocked.status_code == 409
    assert _attempt_rows(database_url) == attempts_before

    finished = client.post(f"/api/practice-sessions/{restarted_body['session_id']}/finish")
    assert finished.status_code == 200
    finished_body = finished.json()
    assert finished_body["session_id"] == restarted_body["session_id"]
    assert finished_body["open"] is False
    assert finished_body["current"] is None
    assert _session_statuses(database_url)[session_id] == "abandoned"
    assert _session_statuses(database_url)[restarted_body["session_id"]] == "closed"
    added = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": migration_at, "end": migration_at + len("migration")},
    )
    assert added.status_code == 201
    assert _attempt_rows(database_url) == attempts_before

    from lait.adapters.http.routers.practice import post_practice_finish, post_practice_start_over

    schema = client.get("/openapi.json").json()
    operation_ids = {
        operation["operationId"]
        for path_item in schema["paths"].values()
        for operation in path_item.values()
        if isinstance(operation, dict) and "operationId" in operation
    }
    assert "practice.finish" in operation_ids
    assert "practice.start_over" in operation_ids

    finish_body = inspect.getsource(post_practice_finish)
    start_over_body = inspect.getsource(post_practice_start_over)
    assert "finish_practice(" in finish_body
    assert "PracticeFinish(" in finish_body
    assert "start_practice(" not in finish_body
    assert "PracticeStart(" not in finish_body
    assert "abandon" not in finish_body.lower()
    assert "start_over_practice(" in start_over_body
    assert "PracticeStartOver(" in start_over_body
    assert "start_practice(" not in start_over_body
    assert "PracticeStart(" not in start_over_body
    assert "abandon" not in start_over_body.lower()
    router_source = Path("backend/lait/adapters/http/routers/practice.py").read_text(
        encoding="utf-8"
    )
    assert "lait.adapters.persistence" not in router_source
    assert "repositories" not in router_source
