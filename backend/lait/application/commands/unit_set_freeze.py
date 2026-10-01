"""Session freeze gate for learning-unit mutations.

Plan 01-05 replaces repositories.has_open_practice_session.
These commands keep calling this function and do not import practice_session.
"""

from __future__ import annotations

from lait.application.ports import LearningUnitRepository
from lait.domain.learning_unit import UnitSetFrozenError


def reject_if_unit_set_frozen(lesson_id: str, units: LearningUnitRepository) -> None:
    if units.has_open_practice_session(lesson_id):
        raise UnitSetFrozenError(lesson_id)
