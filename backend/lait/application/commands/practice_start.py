"""practice.start — freeze the accepted set and open one ordered pass."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.application.queries.practice_get import view_for
from lait.catalog.validation import ModuleRecord
from lait.domain.learning_unit import ACCEPTED
from lait.domain.practice_session import (
    DRAG,
    OPEN,
    TYPED,
    ExerciseDefinition,
    PassItem,
    PracticeSession,
    PracticeView,
    StaleGenerationError,
)

COMMAND_NAME = "practice.start"


@dataclass(frozen=True, slots=True)
class PracticeStart:
    lesson_id: str


def handle(
    command: PracticeStart,
    lessons: LessonRepository,
    units: LearningUnitRepository,
    registry: Sequence[ModuleRecord],
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> PracticeView:
    del registry
    lesson = lessons.get(command.lesson_id)
    if lesson is None:
        raise LessonNotFoundError(command.lesson_id)
    current_ids = _accepted_ids(units, command.lesson_id)
    generation = units.latest_completed_generation(command.lesson_id)  # type: ignore[attr-defined]
    if generation is None or tuple(sorted(generation.accepted_unit_ids)) != current_ids:
        raise StaleGenerationError(command.lesson_id)
    if units.has_open_practice_session(command.lesson_id):
        raise StaleGenerationError(command.lesson_id)

    clock = now or (lambda: datetime.now(UTC))
    mint = new_id or (lambda: str(uuid4()))
    created_at = clock()
    practice = PracticeSession(
        id=mint(),
        lesson_id=command.lesson_id,
        generation_id=generation.id,
        status=OPEN,
        cursor=0,
        items=pass_items_for(generation.definitions),
    )
    units.save_practice_session(practice, created_at)  # type: ignore[attr-defined]
    return view_for(practice, generation)


def pass_items_for(definitions: tuple[ExerciseDefinition, ...]) -> tuple[PassItem, ...]:
    """N>1 walks drag for every unit, then typed. One unit is typed only."""
    ordered = tuple(
        sorted(definitions, key=lambda definition: (definition.start, definition.learning_unit_id))
    )
    modes = (DRAG, TYPED) if len(ordered) > 1 else (TYPED,)
    steps = [(mode, definition) for mode in modes for definition in ordered]
    return tuple(
        PassItem(
            position=index,
            mode=mode,
            learning_unit_id=definition.learning_unit_id,
            definition_id=definition.id,
        )
        for index, (mode, definition) in enumerate(steps)
    )


def _accepted_ids(units: LearningUnitRepository, lesson_id: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            unit.id
            for unit in units.list_units(lesson_id)
            if unit.status == ACCEPTED and unit.removed_at is None
        )
    )
