"""learning_unit.list — live draft and accepted units for one lesson."""

from __future__ import annotations

from lait.application.ports import LearningUnitRepository
from lait.domain.learning_unit import LearningUnit

QUERY_NAME = "learning_unit.list"


def handle(lesson_id: str, units: LearningUnitRepository) -> list[LearningUnit]:
    return units.list_units(lesson_id)
