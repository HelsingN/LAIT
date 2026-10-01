"""Deterministic Gap Fill explanations. Natural alternative stays absent."""

from __future__ import annotations

from lait.domain.exercise import ResultCategory


def explanation(*, category: str, submitted: str, unit: str) -> str:
    if category == "correct":
        return f'Correct. The expected answer is "{unit}".'
    return f'Your answer: "{submitted}". Expected: "{unit}".'


def chunk_record(category: ResultCategory, unit: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if category == "correct":
        return (unit,), ()
    return (), (unit,)
