"""practice.advance — leave a graded item without writing another attempt."""

from __future__ import annotations

from dataclasses import dataclass

from lait.application.ports import LearningUnitRepository
from lait.application.queries.practice_get import view_for
from lait.domain.practice_session import (
    NoCurrentItemError,
    PracticeSessionNotFoundError,
    PracticeView,
    is_open_session,
)

COMMAND_NAME = "practice.advance"


@dataclass(frozen=True, slots=True)
class PracticeAdvance:
    session_id: str
    position: int


def handle(command: PracticeAdvance, units: LearningUnitRepository) -> PracticeView:
    practice = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if practice is None or not is_open_session(practice.status):
        raise PracticeSessionNotFoundError(command.session_id)
    generation = units.get_generation(practice.generation_id)  # type: ignore[attr-defined]
    if generation is None:
        raise PracticeSessionNotFoundError(command.session_id)
    units.advance_current_item(command.session_id, command.position)  # type: ignore[attr-defined]
    moved = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if moved is None:
        raise NoCurrentItemError(command.session_id)
    return view_for(moved, generation)
