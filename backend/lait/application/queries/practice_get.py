"""practice.get — the single current item of an open session."""

from __future__ import annotations

from lait.application.ports import LearningUnitRepository
from lait.domain.practice_session import (
    CurrentItem,
    ExerciseGeneration,
    PracticeSession,
    PracticeSessionNotFoundError,
    PracticeView,
    is_open_session,
)

QUERY_NAME = "practice.get"


def handle(session_id: str, units: LearningUnitRepository) -> PracticeView:
    practice = units.get_practice_session(session_id)  # type: ignore[attr-defined]
    if practice is None:
        raise PracticeSessionNotFoundError(session_id)
    generation = units.get_generation(practice.generation_id)  # type: ignore[attr-defined]
    if generation is None:
        raise PracticeSessionNotFoundError(session_id)
    return view_for(practice, generation)


def view_for(practice: PracticeSession, generation: ExerciseGeneration) -> PracticeView:
    current: CurrentItem | None = None
    if practice.cursor < len(practice.items):
        item = practice.items[practice.cursor]
        definition = next(
            candidate
            for candidate in generation.definitions
            if candidate.id == item.definition_id
        )
        current = CurrentItem(
            mode=item.mode,
            learning_unit_id=item.learning_unit_id,
            exercise_type=definition.exercise_type,
            position=item.position,
            start=definition.start,
            end=definition.end,
            target_text=definition.target_text,
            sentence=definition.sentence,
            segments=definition.segments,
            chip_unit_ids=generation.chip_unit_ids,
        )
    return PracticeView(
        session_id=practice.id,
        lesson_id=practice.lesson_id,
        open=is_open_session(practice.status),
        cursor=practice.cursor,
        current=current,
    )
