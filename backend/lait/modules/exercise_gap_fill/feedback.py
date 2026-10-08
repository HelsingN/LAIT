"""Deterministic Gap Fill explanations. Natural alternative stays absent."""

from __future__ import annotations

from lait.domain.exercise import ResultCategory


def explanation(*, category: str, submitted: str, unit: str) -> str:
    if category == "correct":
        return "The response matches the target for this exercise."
    return "The response does not match the target for this exercise."


def chunk_record(category: ResultCategory, unit: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if category == "correct":
        return (unit,), ()
    return (), (unit,)
