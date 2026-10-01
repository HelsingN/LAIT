"""learning_unit.add — capture one exact source span as a draft unit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.domain.learning_unit import (
    DRAFT,
    LearningUnit,
    MissingSpanError,
    SpanOutOfRangeError,
    SpanOverlapError,
)
from lait.domain.span import Span, overlaps

COMMAND_NAME = "learning_unit.add"


@dataclass(frozen=True, slots=True)
class LearningUnitAdd:
    lesson_id: str
    start: int | None = None
    end: int | None = None


def handle(
    command: LearningUnitAdd,
    lessons: LessonRepository,
    units: LearningUnitRepository,
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> LearningUnit:
    if command.start is None or command.end is None or command.start == command.end:
        raise MissingSpanError("A learning unit requires a non-empty source selection")

    lesson = lessons.get(command.lesson_id)
    if lesson is None:
        raise LessonNotFoundError(command.lesson_id)

    start = command.start
    end = command.end
    source = lesson.source
    if not (0 <= start < end <= len(source)):
        raise SpanOutOfRangeError("Learning unit span is outside the source")

    span = Span(start=start, end=end)
    for existing in units.list_units(command.lesson_id):
        if overlaps(span, Span(start=existing.start, end=existing.end)):
            raise SpanOverlapError("Learning unit span overlaps an existing unit")

    clock = now or (lambda: datetime.now(UTC))
    mint_id = new_id or (lambda: str(uuid4()))
    unit = LearningUnit(
        id=mint_id(),
        lesson_id=command.lesson_id,
        start=start,
        end=end,
        text=source[start:end],
        status=DRAFT,
        created_at=clock(),
        removed_at=None,
    )
    units.add_unit(unit)
    return unit
