"""practice.finish — close the open session and return to the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from lait.application.ports import LearningUnitRepository
from lait.application.queries.practice_get import view_for
from lait.domain.practice_session import (
    CLOSED,
    PracticeSessionNotFoundError,
    PracticeView,
    is_open_session,
)

COMMAND_NAME = "practice.finish"


@dataclass(frozen=True, slots=True)
class PracticeFinish:
    session_id: str


def handle(command: PracticeFinish, units: LearningUnitRepository) -> PracticeView:
    practice = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if practice is None or not is_open_session(practice.status):
        raise PracticeSessionNotFoundError(command.session_id)
    generation = units.get_generation(practice.generation_id)  # type: ignore[attr-defined]
    if generation is None:
        raise PracticeSessionNotFoundError(command.session_id)
    units.set_practice_session_status(command.session_id, CLOSED)  # type: ignore[attr-defined]
    closed = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if closed is None:
        raise PracticeSessionNotFoundError(command.session_id)
    return view_for(closed, generation)
