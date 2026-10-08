"""Smallest contract-valid proof generator. Not part of the learner list."""

from __future__ import annotations

from collections.abc import Sequence

from lait.domain.exercise import AcceptedUnit, ExerciseItem, GenerateResult, PromptSegment


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
    return ExerciseItem(
        learning_unit_id=unit.learning_unit_id,
        exercise_type="proof",
        start=unit.start,
        end=unit.end,
        target_text=unit.text,
        sentence=unit.text,
        segments=(PromptSegment(kind="text", text=unit.text),),
    )
