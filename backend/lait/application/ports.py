"""Repository ports injected into command and query handlers."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from lait.domain.learning_unit import LearningUnit
from lait.domain.lesson import Lesson
from lait.domain.practice_session import PracticeSession


class LessonRepository(Protocol):
    def add(self, lesson: Lesson) -> None: ...

    def get(self, lesson_id: str) -> Lesson | None: ...

    def list_lessons(self) -> list[Lesson]: ...


class LearningUnitRepository(Protocol):
    def add_unit(self, unit: LearningUnit) -> None: ...

    def get_unit(self, unit_id: str) -> LearningUnit | None: ...

    def list_units(self, lesson_id: str) -> list[LearningUnit]: ...

    def save_unit(self, unit: LearningUnit) -> None: ...

    def has_open_practice_session(self, lesson_id: str) -> bool: ...

    def insert_open_practice_session(
        self, practice: PracticeSession, created_at: datetime
    ) -> PracticeSession: ...
