"""HTTP routers map DTOs onto handlers. Application tests do not import the app."""

from __future__ import annotations

import inspect
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient


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


def _practice_snapshot(database_url: str) -> dict[str, list[tuple]]:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        return {
            table: connection.execute(f"select * from {table} order by id").fetchall()
            for table in ("attempts", "practice_sessions", "practice_pass_items")
        }
    finally:
        connection.close()


def test_reopened_http_lists_complete_saved_feedback_without_mutation(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate
    from lait.domain.practice_session import Attempt

    database_url = f"sqlite:///{(tmp_path / 'saved-feedback.db').as_posix()}"
    migrate(database_url)
    original_app = create_app(database_url)
    source = "We are rolling out the migration and will follow through."
    text = "rolling out"
    start = source.index(text)
    with TestClient(original_app) as client:
        created = client.post("/api/lessons", json={"source": source})
        assert created.status_code == 201
        lesson_id = created.json()["id"]
        unit = client.post(
            f"/api/lessons/{lesson_id}/learning-units",
            json={"start": start, "end": start + len(text)},
        )
        assert unit.status_code == 201
        unit_id = unit.json()["id"]
        assert (
            client.post(f"/api/lessons/{lesson_id}/learning-units/{unit_id}/accept").status_code
            == 200
        )
        assert client.post(f"/api/lessons/{lesson_id}/exercises/generate").status_code == 200
        started = client.post("/api/practice-sessions", json={"lesson_id": lesson_id})
        assert started.status_code == 201
        session_id = started.json()["session_id"]

    # Use the public persistence port: the bundled evaluator does not generate alternatives.
    when = datetime(2026, 10, 7, tzinfo=UTC)
    fixtures = [
        (
            "saved-rich",
            "correct",
            "  Rolling out\n👍  ",
            "The target was retrieved; one other chunk was missed.",
            ("rolling out",),
            ("follow through",),
            "deploying the change",
        ),
        (
            "saved-empty",
            "incorrect",
            "  nope\n  ",
            'Your answer: "  nope\n  ". The expected answer is "rolling out".',
            (),
            (),
            None,
        ),
    ]
    for offset, fixture in enumerate(fixtures):
        attempt_id, category, submitted, explanation, used, missed, alternative = fixture
        original_app.state.lesson_repository.add_attempt(
            Attempt(
                id=attempt_id,
                session_id=session_id,
                learning_unit_id=unit_id,
                span_start=start,
                span_end=start + len(text),
                unit_text=text,
                mode="typed",
                submitted=submitted,
                category=category,
                expected=text,
                explanation=explanation,
                chunks_used=used,
                chunks_missed=missed,
                natural_alternative=alternative,
                created_at=when + timedelta(seconds=offset),
            ),
            cursor=0,
        )

    before = _practice_snapshot(database_url)
    # A new app owns a new repository/engine; no cached handler result can satisfy this read.
    with TestClient(create_app(database_url)) as reopened:
        response = reopened.get(f"/api/lessons/{lesson_id}/attempts")
        assert response.status_code == 200
        rows = response.json()["attempts"]
        assert [row["attempt_id"] for row in rows] == [fixture[0] for fixture in fixtures]
        for row, fixture in zip(rows, fixtures, strict=True):
            attempt_id, category, submitted, explanation, used, missed, alternative = fixture
            assert {
                key: row.get(key)
                for key in (
                    "learning_unit_id",
                    "chunks_used",
                    "chunks_missed",
                    "natural_alternative",
                )
            } == {
                "learning_unit_id": unit_id,
                "chunks_used": list(used),
                "chunks_missed": list(missed),
                "natural_alternative": alternative,
            }
            assert row["attempt_id"] == attempt_id
            assert row["session_id"] == session_id
            assert row["category"] == category
            assert row["submitted"] == submitted
            assert row["expected"] == row["unit_text"] == text
            assert row["explanation"] == explanation
            assert (row["span_start"], row["span_end"]) == (start, start + len(text))
            assert row["session_disposition"] == "open"
            assert row["pass_item_count"] == 1
        assert reopened.get(f"/api/lessons/{lesson_id}/attempts").json() == response.json()
        assert reopened.get("/api/lessons/missing-lesson/attempts").status_code == 404
    assert _practice_snapshot(database_url) == before


def test_http_maps_create_dto_and_rejects_empty_source(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate

    database_url = f"sqlite:///{(tmp_path / 'http.db').as_posix()}"
    migrate(database_url)
    client = TestClient(create_app(database_url))

    rejected = client.post("/api/lessons", json={"source": "   "})
    assert rejected.status_code == 422
    assert client.get("/api/lessons").json()["lessons"] == []

    created = client.post(
        "/api/lessons",
        json={"source": "Hello team\nWe shipped the queue.", "title": "Hello team"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["source"] == "Hello team\nWe shipped the queue."
    assert body["title"] == "Hello team"
    assert body["id"]

    listed = client.get("/api/lessons")
    assert listed.status_code == 200
    assert listed.json()["lessons"][0]["id"] == body["id"]

    fetched = client.get(f"/api/lessons/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["source"] == body["source"]

    missing = client.get("/api/lessons/missing-lesson")
    assert missing.status_code == 404

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}


def test_http_maps_learning_unit_dtos(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate

    database_url = f"sqlite:///{(tmp_path / 'http-units.db').as_posix()}"
    migrate(database_url)
    client = TestClient(create_app(database_url))
    created = client.post("/api/lessons", json={"source": "👍out rolling out"})
    assert created.status_code == 201
    lesson_id = created.json()["id"]

    added = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": 1, "end": 4},
    )
    assert added.status_code == 201
    body = added.json()
    assert body["text"] == "out"
    assert body["start"] == 1
    assert body["end"] == 4
    assert body["status"] == "draft"
    unit_id = body["id"]

    listed = client.get(f"/api/lessons/{lesson_id}/learning-units")
    assert listed.status_code == 200
    assert [unit["id"] for unit in listed.json()["learning_units"]] == [unit_id]

    accepted = client.post(f"/api/lessons/{lesson_id}/learning-units/{unit_id}/accept")
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "accepted"

    overlap = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": 2, "end": 4},
    )
    assert overlap.status_code == 422
    after_overlap = client.get(f"/api/lessons/{lesson_id}/learning-units")
    assert [unit["id"] for unit in after_overlap.json()["learning_units"]] == [unit_id]
    assert after_overlap.json()["learning_units"][0]["text"] == "out"

    removed = client.post(f"/api/lessons/{lesson_id}/learning-units/{unit_id}/remove")
    assert removed.status_code == 200
    assert removed.json()["removed_at"] is not None
    assert client.get(f"/api/lessons/{lesson_id}/learning-units").json()["learning_units"] == []

    again = client.post(
        f"/api/lessons/{lesson_id}/learning-units",
        json={"start": 1, "end": 4},
    )
    assert again.status_code == 201
    assert again.json()["id"] != unit_id
    assert again.json()["text"] == "out"

    router_path = Path("backend/lait/adapters/http/routers/learning_units.py")
    router = router_path.read_text(encoding="utf-8")
    assert "learning_unit.add" in router
    assert "learning_unit.remove" in router
    assert "learning_unit.accept" in router
    assert "learning_unit.list" in router
    assert "adapters.persistence" not in router
    assert "sqlalchemy" not in router.lower()
    app_source = Path("backend/lait/adapters/http/app.py").read_text(encoding="utf-8")
    assert "learning_unit" not in app_source

    operation_ids: set[str] = set()
    for path_item in client.get("/openapi.json").json()["paths"].values():
        for operation in path_item.values():
            if isinstance(operation, dict) and "operationId" in operation:
                operation_ids.add(operation["operationId"])
    assert {
        "learning_unit.add",
        "learning_unit.remove",
        "learning_unit.accept",
        "learning_unit.list",
    } <= operation_ids


def test_http_maps_generate_start_get_and_submit_only(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate

    database_url = f"sqlite:///{(tmp_path / 'http.db').as_posix()}"
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
    assert generated.json()["status"] == "completed"
    assert generated.json()["definition_count"] == 1

    started = client.post("/api/practice-sessions", json={"lesson_id": lesson_id})
    assert started.status_code == 201
    session_id = started.json()["session_id"]
    assert started.json()["current"]["mode"] == "typed"
    assert started.json()["open"] is True

    current = client.get(f"/api/practice-sessions/{session_id}")
    assert current.status_code == 200
    assert current.json()["current"]["learning_unit_id"] == accepted.json()["id"]
    assert "items" not in current.json()

    submitted = client.post(
        f"/api/practice-sessions/{session_id}/attempts",
        json={"kind": "typed", "text": "Rolling out"},
    )
    assert submitted.status_code == 200
    body = submitted.json()
    assert body["session_open"] is True
    assert body["category"] == "correct"
    assert body["unit_text"] == text
    assert body["span_start"] == start_at

    listed = client.get(f"/api/lessons/{lesson_id}/attempts")
    assert listed.status_code == 200
    saved = listed.json()["attempts"][0]
    for key in (
        "attempt_id",
        "learning_unit_id",
        "submitted",
        "expected",
        "explanation",
        "chunks_used",
        "chunks_missed",
        "natural_alternative",
    ):
        assert saved[key] == body[key]
    assert saved["natural_alternative"] is None

    nxt = client.get(f"/api/practice-sessions/{session_id}")
    assert nxt.json()["open"] is True
    assert nxt.json()["current"] is None

    schema = client.get("/openapi.json").json()
    operation_ids = {
        operation["operationId"]
        for path in schema["paths"].values()
        for operation in path.values()
        if isinstance(operation, dict) and "operationId" in operation
    }
    assert "exercise.generate" in operation_ids
    assert "practice.start" in operation_ids
    assert "practice.get" in operation_ids
    assert "exercise.submit_attempt" in operation_ids
    practice_router = Path("backend/lait/adapters/http/routers/practice.py").read_text(
        encoding="utf-8"
    )
    assert "lait.adapters.persistence" not in practice_router


def test_http_finish_and_start_over_only_map_dtos(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app
    from lait.adapters.http.routers.practice import post_practice_finish, post_practice_start_over
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
