"""lesson.list / lesson.get and the Lesson List UI contract."""

from __future__ import annotations

from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'lessons.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def test_lesson_list_and_get_round_trip(tmp_path: Path) -> None:
    from lait.application.commands.lesson_create import LessonCreate
    from lait.application.commands.lesson_create import handle as create_lesson
    from lait.application.queries.lesson_get import QUERY_NAME as GET_NAME
    from lait.application.queries.lesson_get import LessonNotFoundError
    from lait.application.queries.lesson_get import handle as get_lesson
    from lait.application.queries.lesson_list import QUERY_NAME as LIST_NAME
    from lait.application.queries.lesson_list import handle as list_lessons

    assert LIST_NAME == "lesson.list"
    assert GET_NAME == "lesson.get"
    repository = _repository(tmp_path)
    created = create_lesson(LessonCreate(source="Open me again."), repository)

    listed = list_lessons(repository)
    assert [lesson.id for lesson in listed] == [created.id]
    assert listed[0].source == "Open me again."
    assert get_lesson(created.id, repository) == created
    with pytest.raises(LessonNotFoundError):
        get_lesson("does-not-exist", repository)


def test_http_routers_delegate_to_handlers_not_repositories() -> None:
    app_source = Path("backend/lait/adapters/http/app.py").read_text(encoding="utf-8")
    assert "include_routers(" in app_source
    routers = Path("backend/lait/adapters/http/routers")
    assert routers.is_dir()
    for path in routers.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "lait.adapters.persistence" not in text
        assert "sqlalchemy" not in text.lower()


def test_lesson_list_ui_locks_copy_and_self_hosted_fonts() -> None:
    # Create copy lives in the form the list page renders.
    page = "\n".join(
        Path(name).read_text(encoding="utf-8")
        for name in (
            "frontend/src/features/lesson/LessonListPage.tsx",
            "frontend/src/features/lesson/CreateLessonForm.tsx",
        )
    )
    workspace = Path("frontend/src/features/lesson/LessonWorkspacePage.tsx").read_text(
        encoding="utf-8"
    )
    tokens = Path("frontend/src/styles/tokens.css").read_text(encoding="utf-8")
    assert "Create Lesson" in page
    assert "Untitled Lesson" in page
    assert "No lessons yet" in page
    assert "Loading…" in page
    assert "Creating…" in page
    assert "Could not create the lesson." in page
    assert "Paste a short English text to create your first lesson" in page
    assert "Could not load this lesson." in workspace
    assert "fonts.googleapis.com" not in tokens
    assert "fonts.gstatic.com" not in tokens
    assert "Source Sans 3" in tokens
    assert "Source Serif 4" in tokens
    woff2 = list(Path("frontend/src/fonts").glob("*.woff2"))
    assert len(woff2) >= 3
