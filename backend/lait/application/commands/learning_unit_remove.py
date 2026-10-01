"""learning_unit.remove — logical delete. The row stays; list omits it."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime

from lait.application.commands.unit_set_freeze import reject_if_unit_set_frozen
from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.domain.learning_unit import LearningUnit, LearningUnitNotFoundError

COMMAND_NAME = "learning_unit.remove"


@dataclass(frozen=True, slots=True)
class LearningUnitRemove:
    lesson_id: str
    unit_id: str


def handle(
    command: LearningUnitRemove,
    lessons: LessonRepository,
    units: LearningUnitRepository,
    *,
    now: Callable[[], datetime] | None = None,
) -> LearningUnit:
    del lessons
    reject_if_unit_set_frozen(command.lesson_id, units)
    unit = units.get_unit(command.unit_id)
    if unit is None or unit.removed_at is not None or unit.lesson_id != command.lesson_id:
        raise LearningUnitNotFoundError(command.unit_id)
    clock = now or (lambda: datetime.now(UTC))
    removed = replace(unit, removed_at=clock())
    units.save_unit(removed)
    return removed
