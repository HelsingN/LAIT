"""Persistence adapter round-trip. Does not start FastAPI."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


def test_repository_persists_lesson_source(tmp_path: Path) -> None:
    from lait.adapters.persistence.database import migrate, open_repository
    from lait.domain.lesson import Lesson

    database_url = f"sqlite:///{(tmp_path / 'persistence.db').as_posix()}"
    migrate(database_url)
    repository = open_repository(database_url)
    created_at = datetime(2026, 10, 2, 12, 0, tzinfo=UTC)
    repository.add(
        Lesson(id="lesson-1", title="Notes", source="rolling out", created_at=created_at)
    )
    loaded = repository.get("lesson-1")
    assert loaded is not None
    assert loaded.id == "lesson-1"
    assert loaded.title == "Notes"
    assert loaded.source == "rolling out"
    assert loaded.created_at == created_at
    assert repository.get("missing") is None
    assert [lesson.id for lesson in repository.list_lessons()] == ["lesson-1"]
