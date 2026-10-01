"""lesson.create — persist one lesson from an exact source paste."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from lait.application.ports import LessonRepository
from lait.domain.lesson import (
    MAX_SOURCE_LENGTH,
    MAX_TITLE_LENGTH,
    EmptyLessonSourceError,
    Lesson,
    LessonSourceTooLongError,
    LessonTitleTooLongError,
    resolve_title,
)

COMMAND_NAME = "lesson.create"


@dataclass(frozen=True, slots=True)
class LessonCreate:
    source: str
    title: str | None = None


def handle(
    command: LessonCreate,
    repository: LessonRepository,
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> Lesson:
    source = command.source
    if source.strip() == "":
        raise EmptyLessonSourceError("Lesson source must not be empty")
    if len(source) > MAX_SOURCE_LENGTH:
        raise LessonSourceTooLongError("Lesson source exceeds the maximum length")

    title = resolve_title(command.title, source)
    if len(title) > MAX_TITLE_LENGTH:
        raise LessonTitleTooLongError("Lesson title exceeds the maximum length")

    clock = now or (lambda: datetime.now(UTC))
    mint_id = new_id or (lambda: str(uuid4()))
    lesson = Lesson(id=mint_id(), title=title, source=source, created_at=clock())
    repository.add(lesson)
    return lesson
