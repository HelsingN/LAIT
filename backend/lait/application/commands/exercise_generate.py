"""exercise.generate — terminal status for learner-visible modules, in one write."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.application.queries.exercise_registry_list_visible import handle as list_visible_for
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.catalog.loader import load_generate
from lait.catalog.validation import ModuleRecord
from lait.domain.exercise import AcceptedUnit
from lait.domain.learning_unit import ACCEPTED
from lait.domain.practice_session import COMPLETED, FAILED, ExerciseDefinition, ExerciseGeneration

COMMAND_NAME = "exercise.generate"


@dataclass(frozen=True, slots=True)
class ExerciseGenerate:
    lesson_id: str


@dataclass(frozen=True, slots=True)
class GenerationOutcome:
    id: str
    lesson_id: str
    status: str
    accepted_unit_ids: tuple[str, ...]
    definition_count: int


def handle(
    command: ExerciseGenerate,
    lessons: LessonRepository,
    units: LearningUnitRepository,
    registry: Sequence[ModuleRecord],
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> GenerationOutcome:
    lesson = lessons.get(command.lesson_id)
    if lesson is None:
        raise LessonNotFoundError(command.lesson_id)

    clock = now or (lambda: datetime.now(UTC))
    mint = new_id or (lambda: str(uuid4()))
    accepted = tuple(
        unit
        for unit in units.list_units(command.lesson_id)
        if unit.status == ACCEPTED and unit.removed_at is None
    )
    accepted_ids = tuple(sorted(unit.id for unit in accepted))
    if not accepted:
        return _store(
            units,
            _generation(
                mint=mint,
                clock=clock,
                lesson_id=command.lesson_id,
                status=FAILED,
                accepted_ids=(),
                chip_ids=(),
                definitions=(),
            ),
        )

    try:
        definitions, chip_ids = _definitions(
            source=lesson.source,
            accepted=accepted,
            registry=registry,
            mint=mint,
        )
    except Exception:
        definitions = ()
        chip_ids = ()
    status = COMPLETED if definitions else FAILED
    stored_ids = accepted_ids if status == COMPLETED else ()
    return _store(
        units,
        _generation(
            mint=mint,
            clock=clock,
            lesson_id=command.lesson_id,
            status=status,
            accepted_ids=stored_ids,
            chip_ids=chip_ids if status == COMPLETED else (),
            definitions=definitions if status == COMPLETED else (),
        ),
    )


def _definitions(
    *,
    source: str,
    accepted: tuple,
    registry: Sequence[ModuleRecord],
    mint: Callable[[], str],
) -> tuple[tuple[ExerciseDefinition, ...], tuple[str, ...]]:
    accepted_units = tuple(
        AcceptedUnit(
            learning_unit_id=unit.id,
            start=unit.start,
            end=unit.end,
            text=unit.text,
        )
        for unit in accepted
    )
    by_id = {module.module_id: module for module in registry}
    definitions: list[ExerciseDefinition] = []
    chip_ids: list[str] = []
    for visible in list_visible_for("learner", registry):
        record = by_id[visible.module_id]
        result = load_generate(record.package)(source, accepted_units)
        for item in result.items:
            definitions.append(
                ExerciseDefinition(
                    id=mint(),
                    learning_unit_id=item.learning_unit_id,
                    exercise_type=item.exercise_type,
                    module_package=record.package,
                    position=len(definitions),
                    start=item.start,
                    end=item.end,
                    target_text=item.target_text,
                    sentence=item.sentence,
                    segments=item.segments,
                )
            )
        for chip_id in result.chip_unit_ids:
            if chip_id not in chip_ids:
                chip_ids.append(chip_id)
    return tuple(definitions), tuple(chip_ids)


def _generation(
    *,
    mint: Callable[[], str],
    clock: Callable[[], datetime],
    lesson_id: str,
    status: str,
    accepted_ids: tuple[str, ...],
    chip_ids: tuple[str, ...],
    definitions: tuple[ExerciseDefinition, ...],
) -> ExerciseGeneration:
    return ExerciseGeneration(
        id=mint(),
        lesson_id=lesson_id,
        status=status,
        accepted_unit_ids=accepted_ids,
        chip_unit_ids=chip_ids,
        created_at=clock(),
        definitions=definitions,
    )


def _store(units: LearningUnitRepository, generation: ExerciseGeneration) -> GenerationOutcome:
    units.save_generation(generation)  # type: ignore[attr-defined]
    return GenerationOutcome(
        id=generation.id,
        lesson_id=generation.lesson_id,
        status=generation.status,
        accepted_unit_ids=generation.accepted_unit_ids,
        definition_count=len(generation.definitions),
    )
