"""One open practice session row per lesson. Does not start FastAPI."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from lait.domain.practice_session import OPEN, PracticeSession


def _database(tmp_path: Path) -> tuple[object, str]:
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'practice.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url), database_url


def _connect(database_url: str) -> sqlite3.Connection:
    return sqlite3.connect(database_url.removeprefix("sqlite:///"))


def _seed_lesson_and_generation(database_url: str) -> None:
    connection = _connect(database_url)
    try:
        connection.execute(
            "insert into lessons (id, title, source, created_at) values (?, ?, ?, ?)",
            ("lesson-1", "Notes", "alpha", "2026-10-02T00:00:00+00:00"),
        )
        connection.execute(
            """
            insert into exercise_generations
                (id, lesson_id, status, accepted_unit_ids, chip_unit_ids, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            ("generation-1", "lesson-1", "completed", "[]", "[]", "2026-10-02T00:00:00+00:00"),
        )
        connection.commit()
    finally:
        connection.close()


def _insert_session(database_url: str, session_id: str, status: str) -> None:
    connection = _connect(database_url)
    try:
        connection.execute(
            """
            insert into practice_sessions
                (id, lesson_id, generation_id, status, cursor, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            (session_id, "lesson-1", "generation-1", status, 0, "2026-10-02T00:00:00+00:00"),
        )
        connection.commit()
    finally:
        connection.close()


def test_partial_unique_index_rejects_a_second_open_row(tmp_path: Path) -> None:
    _repository, database_url = _database(tmp_path)
    _seed_lesson_and_generation(database_url)
    _insert_session(database_url, "first-open", "open")

    with pytest.raises(sqlite3.IntegrityError):
        _insert_session(database_url, "second-open", "open")

    _insert_session(database_url, "closed-row", "closed")

    connection = _connect(database_url)
    try:
        index_row = connection.execute(
            "select sql from sqlite_master where type = 'index' and name = ?",
            ("uq_practice_sessions_one_open_per_lesson",),
        ).fetchone()
        open_ids = connection.execute(
            "select id from practice_sessions where status = 'open' order by id"
        ).fetchall()
    finally:
        connection.close()

    assert index_row is not None
    assert "uq_practice_sessions_one_open_per_lesson" in index_row[0]
    assert open_ids == [("first-open",)]


def test_insert_open_practice_session_returns_the_existing_open_row(tmp_path: Path) -> None:
    repository, database_url = _database(tmp_path)
    _seed_lesson_and_generation(database_url)
    _insert_session(database_url, "winner-open", "open")

    stored = repository.insert_open_practice_session(
        PracticeSession(
            id="minted-id",
            lesson_id="lesson-1",
            generation_id="generation-1",
            status=OPEN,
            cursor=0,
            items=(),
        ),
        datetime(2026, 10, 2, tzinfo=UTC),
    )

    connection = _connect(database_url)
    try:
        ids = connection.execute(
            "select id from practice_sessions order by id"
        ).fetchall()
    finally:
        connection.close()

    assert stored.id == "winner-open"
    assert ids == [("winner-open",)]
