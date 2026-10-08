"""Lesson identity, immutable source, and title metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

UNTITLED_LESSON = "Untitled Lesson"
MAX_SOURCE_LENGTH = 100_000
MAX_TITLE_LENGTH = 200

_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")


class EmptyLessonSourceError(ValueError):
    """Raised when source is empty or whitespace-only. No lesson row is written."""


class LessonSourceTooLongError(ValueError):
    """Raised when source exceeds the code-point bound. No lesson row is written."""


class LessonTitleTooLongError(ValueError):
    """Raised when a provided title exceeds the metadata bound."""


@dataclass(frozen=True, slots=True)
class Lesson:
    id: str
    title: str
    source: str
    created_at: datetime


def suggest_title(source: str) -> str:
    """First meaningful line, with a leading markdown heading marker removed."""
    for raw_line in source.splitlines():
        candidate = _HEADING.sub("", raw_line.strip()).strip()
        if any(character.isalnum() for character in candidate):
            return candidate[:MAX_TITLE_LENGTH]
    return UNTITLED_LESSON


def resolve_title(requested: str | None, source: str) -> str:
    """None asks for a suggestion. A blank string stores Untitled Lesson."""
    if requested is None:
        return suggest_title(source)
    stripped = requested.strip()
    if not stripped:
        return UNTITLED_LESSON
    return stripped
