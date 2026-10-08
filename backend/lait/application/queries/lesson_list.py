"""lesson.list — active lessons, newest first."""

from __future__ import annotations

from lait.application.ports import LessonRepository
from lait.domain.lesson import Lesson

QUERY_NAME = "lesson.list"


def handle(repository: LessonRepository) -> list[Lesson]:
    return repository.list_lessons()
