"""lesson.create behavior: exact paste, validation, distinct ids, DTO mapping."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'lessons.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def test_lesson_create_persists_exact_utf8_source(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import COMMAND_NAME, LessonCreate, handle
    from lait.application.queries.lesson_get import handle as get_lesson

    source = "cafe\u0301 — naïve 😀\n  keep surrounding space  \n"
    repository = _repository(tmp_path)
    created = handle(LessonCreate(source=source), repository)

    assert COMMAND_NAME == "lesson.create"
    assert created.source == source
    assert created.id
    assert created.title == "cafe\u0301 — naïve 😀"
    fetched = get_lesson(created.id, repository)
    assert fetched.source == source
    assert fetched.id == created.id


def test_whitespace_only_source_writes_no_row(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.application.queries.lesson_list import handle as list_lessons
    from lait.domain.lesson import EmptyLessonSourceError

    repository = _repository(tmp_path)
    with pytest.raises(EmptyLessonSourceError):
        handle(LessonCreate(source=" \n\t  "), repository)
    assert list_lessons(repository) == []


def test_source_over_max_length_writes_no_row(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.application.queries.lesson_list import handle as list_lessons
    from lait.domain.lesson import MAX_SOURCE_LENGTH, LessonSourceTooLongError

    repository = _repository(tmp_path)
    with pytest.raises(LessonSourceTooLongError):
        handle(LessonCreate(source="a" * (MAX_SOURCE_LENGTH + 1)), repository)
    assert list_lessons(repository) == []


def test_same_paste_twice_creates_distinct_immutable_ids(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.application.queries.lesson_list import handle as list_lessons

    repository = _repository(tmp_path)
    source = "The migration shipped on Tuesday."
    first = handle(LessonCreate(source=source), repository)
    second = handle(LessonCreate(source=source), repository)

    assert first.id != second.id
    assert first.source == second.source == source
    assert {lesson.id for lesson in list_lessons(repository)} == {first.id, second.id}


def test_omitted_title_uses_first_meaningful_line(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle

    repository = _repository(tmp_path)
    source = "\n\n# Ship notes\n\nWe migrated the queue."
    created = handle(LessonCreate(source=source), repository)

    assert created.title == "Ship notes"
    assert created.source == source


def test_blank_title_stores_untitled_lesson(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.domain.lesson import UNTITLED_LESSON

    repository = _repository(tmp_path)
    created = handle(
        LessonCreate(source="A real opening line.", title="   "),
        repository,
    )
    assert created.title == UNTITLED_LESSON == "Untitled Lesson"


def test_explicit_title_is_trimmed_and_not_replaced(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle

    repository = _repository(tmp_path)
    created = handle(
        LessonCreate(source="Body that would suggest another title", title="  Interview notes  "),
        repository,
    )
    assert created.title == "Interview notes"


def test_punctuation_only_source_suggests_untitled_lesson(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.domain.lesson import UNTITLED_LESSON

    repository = _repository(tmp_path)
    created = handle(LessonCreate(source="???\n---"), repository)
    assert created.title == UNTITLED_LESSON


def test_application_handlers_do_not_import_fastapi_or_sqlalchemy() -> None:
    root = Path(__file__).resolve().parents[2] / "lait" / "application"
    assert root.is_dir()
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        if "fastapi" in text or "sqlalchemy" in text:
            offenders.append(str(path))
    assert offenders == []


def test_http_maps_create_dto_and_rejects_empty_source(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

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


def test_list_orders_by_created_at_desc_then_id(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate, handle
    from lait.application.queries.lesson_list import handle as list_lessons

    repository = _repository(tmp_path)
    same_instant = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
    later = datetime(2026, 10, 2, 12, 0, tzinfo=UTC)
    ids = iter(["b-lesson", "a-lesson", "newer-lesson"])

    handle(
        LessonCreate(source="older b"),
        repository,
        now=lambda: same_instant,
        new_id=lambda: next(ids),
    )
    handle(
        LessonCreate(source="older a"),
        repository,
        now=lambda: same_instant,
        new_id=lambda: next(ids),
    )
    handle(
        LessonCreate(source="newer"),
        repository,
        now=lambda: later,
        new_id=lambda: next(ids),
    )

    assert [lesson.id for lesson in list_lessons(repository)] == [
        "newer-lesson",
        "a-lesson",
        "b-lesson",
    ]
