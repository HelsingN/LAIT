"""Public exercise contract. Modules implement it; core does not name module ids."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ResultCategory = Literal["correct", "acceptable", "partial", "incorrect", "uncertain"]

RESULT_CATEGORIES: tuple[ResultCategory, ...] = (
    "correct",
    "acceptable",
    "partial",
    "incorrect",
    "uncertain",
)


@dataclass(frozen=True, slots=True)
class AcceptedUnit:
    learning_unit_id: str
    start: int
    end: int
    text: str


@dataclass(frozen=True, slots=True)
class PromptSegment:
    kind: str
    text: str


@dataclass(frozen=True, slots=True)
class ExerciseItem:
    learning_unit_id: str
    exercise_type: str
    start: int
    end: int
    target_text: str
    sentence: str
    segments: tuple[PromptSegment, ...]


@dataclass(frozen=True, slots=True)
class GenerateResult:
    items: tuple[ExerciseItem, ...]
    chip_unit_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DragAnswer:
    learning_unit_id: str
    text: str


@dataclass(frozen=True, slots=True)
class TypedAnswer:
    text: str


@dataclass(frozen=True, slots=True)
class Evaluation:
    category: ResultCategory
    submitted: str
    expected: str
    explanation: str
    chunks_used: tuple[str, ...]
    chunks_missed: tuple[str, ...]
    natural_alternative: str | None
