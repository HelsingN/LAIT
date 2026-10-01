"""Smallest contract-valid proof grader. Drag uses unit identity."""

from __future__ import annotations

from lait.domain.exercise import DragAnswer, Evaluation, ExerciseItem, TypedAnswer


def evaluate(item: ExerciseItem, answer: DragAnswer | TypedAnswer) -> Evaluation:
    if isinstance(answer, DragAnswer):
        matched = answer.learning_unit_id == item.learning_unit_id
        submitted = answer.text
    elif isinstance(answer, TypedAnswer):
        matched = answer.text == item.target_text
        submitted = answer.text
    else:
        raise TypeError("answer must be a drag or typed submission")
    category = "correct" if matched else "incorrect"
    if matched:
        used: tuple[str, ...] = (item.target_text,)
        missed: tuple[str, ...] = ()
        message = f'Correct. "{item.target_text}".'
    else:
        used = ()
        missed = (item.target_text,)
        message = f'Incorrect. "{submitted}".'
    return Evaluation(
        category=category,
        submitted=submitted,
        expected=item.target_text,
        explanation=message,
        chunks_used=used,
        chunks_missed=missed,
        natural_alternative=None,
    )
