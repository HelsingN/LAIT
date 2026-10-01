"""Source spans addressed by Unicode code points (Python str indices)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Span:
    start: int
    end: int


def overlaps(left: Span, right: Span) -> bool:
    """True when the spans share a code point. Touching edges do not overlap."""
    return left.start < right.end and right.start < left.end
