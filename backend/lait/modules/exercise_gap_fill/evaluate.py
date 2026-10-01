"""Server-side Gap Fill grading. Drag uses unit identity, never chip text."""

from __future__ import annotations

from lait.domain.exercise import DragAnswer, Evaluation, ExerciseItem, TypedAnswer
from lait.modules.exercise_gap_fill.feedback import chunk_record, explanation


def typed_match(submitted: str, unit_text: str) -> bool:
    return submitted.strip().casefold() == unit_text.strip().casefold()


def evaluate(item: ExerciseItem, answer: DragAnswer | TypedAnswer) -> Evaluation:
    if isinstance(answer, DragAnswer):
        matched = answer.learning_unit_id == item.learning_unit_id
        submitted = answer.text
    elif isinstance(answer, TypedAnswer):
        matched = typed_match(answer.text, item.target_text)
        submitted = answer.text
    else:
        raise TypeError("answer must be a drag or typed submission")
    category = "correct" if matched else "incorrect"
    used, missed = chunk_record(category, item.target_text)
    return Evaluation(
        category=category,
        submitted=submitted,
        expected=item.target_text,
        explanation=explanation(category=category, submitted=submitted, unit=item.target_text),
        chunks_used=used,
        chunks_missed=missed,
        natural_alternative=None,
    )
