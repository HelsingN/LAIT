"""exercise.latest_completed — a completed generation only when the accepted set still matches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from lait.application.queries.lesson_get import LessonNotFoundError
from lait.domain.learning_unit import ACCEPTED, LearningUnit
from lait.domain.lesson import Lesson
from lait.domain.practice_session import COMPLETED, ExerciseGeneration

QUERY_NAME = "exercise.latest_completed"


@dataclass(frozen=True, slots=True)
class LatestCompleted:
    restorable: bool
    generation_id: str | None
    accepted_unit_ids: tuple[str, ...]


class LatestCompletedRepository(Protocol):
    def get(self, lesson_id: str) -> Lesson | None: ...

    def list_units(self, lesson_id: str) -> list[LearningUnit]: ...

    def latest_completed_generation(self, lesson_id: str) -> ExerciseGeneration | None: ...


def handle(lesson_id: str, repository: LatestCompletedRepository) -> LatestCompleted:
    if repository.get(lesson_id) is None:
        raise LessonNotFoundError(lesson_id)
    latest = repository.latest_completed_generation(lesson_id)
    current_ids = _accepted_ids(repository.list_units(lesson_id))
    if (
        latest is None
        or latest.status != COMPLETED
        or tuple(sorted(latest.accepted_unit_ids)) != current_ids
    ):
        return LatestCompleted(restorable=False, generation_id=None, accepted_unit_ids=())
    return LatestCompleted(
        restorable=True,
        generation_id=latest.id,
        accepted_unit_ids=latest.accepted_unit_ids,
    )


def _accepted_ids(units: list[LearningUnit]) -> tuple[str, ...]:
    return tuple(
        sorted(unit.id for unit in units if unit.status == ACCEPTED and unit.removed_at is None)
    )
