"""exercise.submit_attempt — persist an Attempt, then return server-side feedback."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from lait.application.ports import LearningUnitRepository
from lait.catalog.loader import load_evaluate
from lait.catalog.validation import ModuleRecord
from lait.domain.exercise import DragAnswer, ExerciseItem, TypedAnswer
from lait.domain.learning_unit import LearningUnitNotFoundError
from lait.domain.practice_session import (
    DRAG,
    TYPED,
    Attempt,
    NoCurrentItemError,
    PassItem,
    PracticeSession,
    PracticeSessionNotFoundError,
)

COMMAND_NAME = "exercise.submit_attempt"


@dataclass(frozen=True, slots=True)
class SubmitAttempt:
    session_id: str
    kind: str
    text: str
    submitted_unit_id: str | None = None
    target_learning_unit_id: str | None = None


@dataclass(frozen=True, slots=True)
class SubmitResult:
    attempt_id: str
    session_open: bool
    cursor: int
    category: str
    submitted: str
    expected: str
    explanation: str
    chunks_used: tuple[str, ...]
    chunks_missed: tuple[str, ...]
    natural_alternative: str | None
    learning_unit_id: str
    span_start: int
    span_end: int
    unit_text: str


def handle(
    command: SubmitAttempt,
    units: LearningUnitRepository,
    registry: Sequence[ModuleRecord],
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> SubmitResult:
    del registry
    practice = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if practice is None or not practice.status == "open":
        raise PracticeSessionNotFoundError(command.session_id)
    item, advance = _resolve_item(practice, command)
    generation = units.get_generation(practice.generation_id)  # type: ignore[attr-defined]
    if generation is None:
        raise PracticeSessionNotFoundError(command.session_id)
    definition = next(
        candidate for candidate in generation.definitions if candidate.id == item.definition_id
    )
    unit = units.get_unit(item.learning_unit_id)
    if unit is None:
        raise LearningUnitNotFoundError(item.learning_unit_id)
    if command.kind == DRAG:
        answer = DragAnswer(
            learning_unit_id=command.submitted_unit_id or "",
            text=command.text,
        )
    elif command.kind == TYPED:
        answer = TypedAnswer(text=command.text)
    else:
        raise NoCurrentItemError(command.session_id)
    evaluation = load_evaluate(definition.module_package)(definition_to_item(definition), answer)
    clock = now or (lambda: datetime.now(UTC))
    mint = new_id or (lambda: str(uuid4()))
    prior = units.list_attempt_keys_for_session(practice.id)  # type: ignore[attr-defined]
    prior_incorrect = any(
        unit_id == item.learning_unit_id and mode == item.mode and category == "incorrect"
        for _attempt_id, unit_id, mode, category in prior
    )
    category = evaluation.category
    if category == "correct" and prior_incorrect:
        category = "corrected"
    cursor = practice.cursor
    attempt = Attempt(
        id=mint(),
        session_id=practice.id,
        learning_unit_id=unit.id,
        span_start=unit.start,
        span_end=unit.end,
        unit_text=unit.text,
        mode=item.mode,
        submitted=evaluation.submitted,
        category=category,
        expected=evaluation.expected,
        explanation=evaluation.explanation,
        chunks_used=evaluation.chunks_used,
        chunks_missed=evaluation.chunks_missed,
        natural_alternative=evaluation.natural_alternative,
        created_at=clock(),
    )
    units.add_attempt(attempt, cursor)  # type: ignore[attr-defined]
    if advance and category in {"correct", "corrected"}:
        cursor = units.advance_current_item(practice.id, practice.cursor)  # type: ignore[attr-defined]
    return SubmitResult(
        attempt_id=attempt.id,
        session_open=True,
        cursor=cursor,
        category=attempt.category,
        submitted=attempt.submitted,
        expected=attempt.expected,
        explanation=attempt.explanation,
        chunks_used=attempt.chunks_used,
        chunks_missed=attempt.chunks_missed,
        natural_alternative=attempt.natural_alternative,
        learning_unit_id=attempt.learning_unit_id,
        span_start=attempt.span_start,
        span_end=attempt.span_end,
        unit_text=attempt.unit_text,
    )


def definition_to_item(definition) -> ExerciseItem:
    return ExerciseItem(
        learning_unit_id=definition.learning_unit_id,
        exercise_type=definition.exercise_type,
        start=definition.start,
        end=definition.end,
        target_text=definition.target_text,
        sentence=definition.sentence,
        segments=definition.segments,
    )


def _resolve_item(practice: PracticeSession, command: SubmitAttempt) -> tuple[PassItem, bool]:
    if command.target_learning_unit_id is None:
        if practice.cursor >= len(practice.items):
            raise NoCurrentItemError(practice.id)
        return practice.items[practice.cursor], True
    if practice.cursor < len(practice.items):
        current = practice.items[practice.cursor]
        if (
            current.learning_unit_id == command.target_learning_unit_id
            and current.mode == command.kind
        ):
            return current, True
    past = [
        item
        for item in practice.items
        if item.learning_unit_id == command.target_learning_unit_id
        and item.mode == command.kind
        and item.position < practice.cursor
    ]
    if not past:
        raise NoCurrentItemError(practice.id)
    return past[0], False
