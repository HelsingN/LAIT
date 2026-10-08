"""learning_unit.accept — move a draft unit into the accepted pool."""

from __future__ import annotations

from dataclasses import dataclass, replace

from lait.application.commands.unit_set_freeze import reject_if_unit_set_frozen
from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.domain.learning_unit import ACCEPTED, DRAFT, LearningUnit, LearningUnitNotFoundError

COMMAND_NAME = "learning_unit.accept"


@dataclass(frozen=True, slots=True)
class LearningUnitAccept:
    lesson_id: str
    unit_id: str


def handle(
    command: LearningUnitAccept,
    lessons: LessonRepository,
    units: LearningUnitRepository,
) -> LearningUnit:
    del lessons
    reject_if_unit_set_frozen(command.lesson_id, units)
    unit = units.get_unit(command.unit_id)
    if unit is None or unit.removed_at is not None or unit.lesson_id != command.lesson_id:
        raise LearningUnitNotFoundError(command.unit_id)
    if unit.status != DRAFT:
        raise LearningUnitNotFoundError(command.unit_id)
    accepted = replace(unit, status=ACCEPTED)
    units.save_unit(accepted)
    return accepted
