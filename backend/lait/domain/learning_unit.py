"""Manual learning unit linked to one source occurrence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

DRAFT = "draft"
ACCEPTED = "accepted"


class MissingSpanError(ValueError):
    """Raised when add has no selection. No learning-unit row is written."""


class SpanOutOfRangeError(ValueError):
    """Raised when code-point offsets fall outside the source. No row is written."""


class SpanOverlapError(ValueError):
    """Raised when a span overlaps a live unit. The existing unit stays."""


class LearningUnitNotFoundError(LookupError):
    def __init__(self, unit_id: str) -> None:
        super().__init__(unit_id)
        self.unit_id = unit_id


class UnitSetFrozenError(RuntimeError):
    """Raised when a practice session has frozen the lesson's unit set."""

    def __init__(self, lesson_id: str) -> None:
        super().__init__(lesson_id)
        self.lesson_id = lesson_id


@dataclass(frozen=True, slots=True)
class LearningUnit:
    id: str
    lesson_id: str
    start: int
    end: int
    text: str
    status: str
    created_at: datetime
    removed_at: datetime | None = None
