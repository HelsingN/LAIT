"""lesson.get — one lesson by immutable id."""

from __future__ import annotations

from lait.application.ports import LessonRepository
from lait.domain.lesson import Lesson

QUERY_NAME = "lesson.get"


class LessonNotFoundError(LookupError):
    def __init__(self, lesson_id: str) -> None:
        super().__init__(lesson_id)
        self.lesson_id = lesson_id


def handle(lesson_id: str, repository: LessonRepository) -> Lesson:
    lesson = repository.get(lesson_id)
    if lesson is None:
        raise LessonNotFoundError(lesson_id)
    return lesson
