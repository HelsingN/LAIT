"""Saved generation and attempts round-trip through the repository after migrate."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

LEGACY_EXPLANATION = 'Correct. The expected answer is "alpha". 👍'
SAVED_USED = ("alpha", "naïve 👍", "alpha")
SAVED_MISSED = ("follow through",)
SAVED_ALTERNATIVE = "deploying the change"


def _database(tmp_path: Path) -> tuple[object, str]:
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'reopen.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url), database_url


def _connect(database_url: str) -> sqlite3.Connection:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def _seed(database_url: str) -> None:
    connection = _connect(database_url)
    try:
        connection.execute(
            "insert into lessons (id, title, source, created_at) values (?, ?, ?, ?)",
            ("lesson-1", "Notes", "alpha beta", "2026-10-02T00:00:00+00:00"),
        )
        connection.execute(
            """
            insert into learning_units
                (id, lesson_id, span_start, span_end, text, status, removed_at, created_at)
            values (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("unit-1", "lesson-1", 0, 5, "alpha", "accepted", None, "2026-10-02T00:00:00+00:00"),
        )
        connection.execute(
            """
            insert into exercise_generations
                (id, lesson_id, status, accepted_unit_ids, chip_unit_ids, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                "generation-1",
                "lesson-1",
                "completed",
                '["unit-1"]',
                '["unit-1"]',
                "2026-10-02T00:00:00+00:00",
            ),
        )
        connection.execute(
            """
            insert into exercise_definitions (
                id, generation_id, position, learning_unit_id, exercise_type, module_package,
                span_start, span_end, target_text, sentence, segments
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "definition-1",
                "generation-1",
                0,
                "unit-1",
                "gap-fill",
                "official.exercise.gap-fill",
                0,
                5,
                "alpha",
                "_____",
                "[]",
            ),
        )
        connection.executemany(
            """
            insert into practice_sessions
                (id, lesson_id, generation_id, status, cursor, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "session-done",
                    "lesson-1",
                    "generation-1",
                    "closed",
                    2,
                    "2026-10-02T00:00:00+00:00",
                ),
                (
                    "session-early",
                    "lesson-1",
                    "generation-1",
                    "closed",
                    1,
                    "2026-10-02T01:00:00+00:00",
                ),
            ],
        )
        connection.executemany(
            """
            insert into practice_pass_items
                (id, session_id, position, mode, learning_unit_id, definition_id)
            values (?, ?, ?, ?, ?, ?)
            """,
            [
                ("done-0", "session-done", 0, "drag", "unit-1", "definition-1"),
                ("done-1", "session-done", 1, "typed", "unit-1", "definition-1"),
                ("early-0", "session-early", 0, "drag", "unit-1", "definition-1"),
                ("early-1", "session-early", 1, "typed", "unit-1", "definition-1"),
            ],
        )
        connection.executemany(
            """
            insert into attempts (
                id, session_id, learning_unit_id, span_start, span_end, unit_text, mode,
                submitted, category, expected, explanation, chunks_used, chunks_missed,
                natural_alternative, created_at
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "attempt-done",
                    "session-done",
                    "unit-1",
                    0,
                    5,
                    "alpha",
                    "drag",
                    "alpha",
                    "correct",
                    "alpha",
                    LEGACY_EXPLANATION,
                    '["alpha", "naïve 👍", "alpha"]',
                    '["follow through"]',
                    SAVED_ALTERNATIVE,
                    "2026-10-02T00:01:00+00:00",
                ),
                (
                    "attempt-early",
                    "session-early",
                    "unit-1",
                    0,
                    5,
                    "alpha",
                    "typed",
                    "nope",
                    "incorrect",
                    "alpha",
                    "missed",
                    "[]",
                    "[]",
                    None,
                    "2026-10-02T01:01:00+00:00",
                ),
            ],
        )
        connection.commit()
    finally:
        connection.close()


def test_repository_reads_matching_generation_and_pass_dispositions(tmp_path: Path) -> None:
    from lait.adapters.persistence.database import open_repository
    from lait.application.queries.attempt_list_for_lesson import handle as list_attempts
    from lait.application.queries.exercise_latest_completed import handle as latest_completed

    _original, database_url = _database(tmp_path)
    _seed(database_url)
    repository = open_repository(database_url)

    latest = latest_completed("lesson-1", repository)
    listed = list_attempts("lesson-1", repository)

    assert latest.restorable is True
    assert latest.generation_id == "generation-1"
    assert latest.accepted_unit_ids == ("unit-1",)
    assert [
        (row.session_id, row.session_disposition, row.mode) for row in listed.attempts
    ] == [
        ("session-done", "completed", "drag"),
        ("session-early", "exited", "typed"),
    ]
    rich, empty = listed.attempts
    assert rich.attempt_id == "attempt-done"
    assert rich.learning_unit_id == empty.learning_unit_id == "unit-1"
    assert rich.explanation == LEGACY_EXPLANATION
    assert rich.chunks_used == SAVED_USED
    assert rich.chunks_missed == SAVED_MISSED
    assert rich.natural_alternative == SAVED_ALTERNATIVE
    assert empty.chunks_used == empty.chunks_missed == ()
    assert empty.natural_alternative is None
    assert empty.explanation == "missed"


def test_reopened_repository_preserves_complete_feedback_records(tmp_path: Path) -> None:
    from lait.adapters.persistence.database import open_repository

    _original, database_url = _database(tmp_path)
    _seed(database_url)
    with closing(_connect(database_url)) as connection:
        before = {
            table: connection.execute(f"select * from {table} order by id").fetchall()
            for table in ("attempts", "practice_sessions", "practice_pass_items")
        }
    reopened = open_repository(database_url)
    records = reopened.list_attempt_records_for_lesson("lesson-1")
    assert [record.attempt_id for record in records] == ["attempt-done", "attempt-early"]
    rich, empty = records
    assert rich.learning_unit_id == empty.learning_unit_id == "unit-1"
    assert rich.chunks_used == SAVED_USED
    assert rich.chunks_missed == SAVED_MISSED
    assert rich.natural_alternative == SAVED_ALTERNATIVE
    assert rich.explanation == LEGACY_EXPLANATION
    assert rich.submitted == rich.expected == rich.unit_text == "alpha"
    assert (rich.span_start, rich.span_end) == (0, 5)
    assert (rich.cursor, rich.pass_item_count, rich.session_item_count) == (2, 1, 2)
    assert rich.session_status == "closed"
    assert empty.chunks_used == empty.chunks_missed == ()
    assert empty.natural_alternative is None
    assert empty.submitted == "nope"
    assert empty.expected == empty.unit_text == "alpha"
    assert empty.explanation == "missed"
    assert reopened.list_attempt_records_for_lesson("lesson-1") == records
    with closing(_connect(database_url)) as connection:
        after = {
            table: connection.execute(f"select * from {table} order by id").fetchall()
            for table in ("attempts", "practice_sessions", "practice_pass_items")
        }
    assert after == before


@pytest.mark.parametrize("column", ["chunks_used", "chunks_missed"])
@pytest.mark.parametrize("raw", ["not-json", "null", "{}", '"alpha"', "[1]", '["alpha", null]'])
def test_reopened_repository_rejects_malformed_saved_chunks(
    tmp_path: Path, column: str, raw: str
) -> None:
    from lait.adapters.persistence.database import open_repository

    _original, database_url = _database(tmp_path)
    _seed(database_url)
    with closing(_connect(database_url)) as connection:
        connection.execute(f"update attempts set {column} = ? where id = ?", (raw, "attempt-done"))
        connection.commit()
    reopened = open_repository(database_url)
    with pytest.raises(ValueError):
        reopened.list_attempt_records_for_lesson("lesson-1")
    with closing(_connect(database_url)) as connection:
        assert connection.execute(
            f"select {column} from attempts where id = ?", ("attempt-done",)
        ).fetchone() == (raw,)
