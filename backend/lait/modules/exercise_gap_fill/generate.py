"""Gap Fill definitions. Each accepted unit blanks only its own span."""

from __future__ import annotations

from collections.abc import Sequence

from lait.domain.exercise import (
    AcceptedUnit,
    ExerciseItem,
    GenerateResult,
    PromptSegment,
)
from lait.modules.exercise_gap_fill.sentence_window import sentence_window

BLANK = "______"


def generate(source: str, units: Sequence[AcceptedUnit]) -> GenerateResult:
    ordered = tuple(sorted(units, key=lambda unit: (unit.start, unit.learning_unit_id)))
    return GenerateResult(
        items=tuple(_item_for(source, unit) for unit in ordered),
        chip_unit_ids=tuple(unit.learning_unit_id for unit in ordered),
    )


def _item_for(source: str, unit: AcceptedUnit) -> ExerciseItem:
    if unit.start < 0 or unit.end > len(source) or unit.start > unit.end:
        raise ValueError("unit span is outside the source")
    if source[unit.start : unit.end] != unit.text:
        raise ValueError("unit text does not match the source span")
    window_start, window_end = sentence_window(source, unit.start, unit.end)
    before = source[window_start : unit.start]
    after = source[unit.end : window_end]
    segments: list[PromptSegment] = []
    if before:
        segments.append(PromptSegment(kind="text", text=before))
    segments.append(PromptSegment(kind="blank", text=BLANK))
    if after:
        segments.append(PromptSegment(kind="text", text=after))
    return ExerciseItem(
        learning_unit_id=unit.learning_unit_id,
        exercise_type="gap-fill",
        start=unit.start,
        end=unit.end,
        target_text=unit.text,
        sentence="".join(segment.text for segment in segments),
        segments=tuple(segments),
    )
