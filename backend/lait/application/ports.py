"""Repository ports injected into command and query handlers."""

from __future__ import annotations

from typing import Protocol

from lait.domain.lesson import Lesson


class LessonRepository(Protocol):
    def add(self, lesson: Lesson) -> None: ...

    def get(self, lesson_id: str) -> Lesson | None: ...

    def list_lessons(self) -> list[Lesson]: ...
