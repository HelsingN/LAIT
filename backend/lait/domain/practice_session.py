"""Practice session, generation snapshot, and recorded attempts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from lait.domain.exercise import PromptSegment

OPEN = "open"
COMPLETED = "completed"
FAILED = "failed"
DRAG = "drag"
TYPED = "typed"


def is_open_session(status: str) -> bool:
    return status == OPEN


class StaleGenerationError(RuntimeError):
    """Raised when practice.start sees a different accepted-unit id set."""

    def __init__(self, lesson_id: str) -> None:
        super().__init__(lesson_id)
        self.lesson_id = lesson_id


class PracticeSessionNotFoundError(LookupError):
    def __init__(self, session_id: str) -> None:
        super().__init__(session_id)
        self.session_id = session_id


class NoCurrentItemError(RuntimeError):
    """Raised when submit does not name a reached item in the open session."""

    def __init__(self, session_id: str) -> None:
        super().__init__(session_id)
        self.session_id = session_id


@dataclass(frozen=True, slots=True)
class ExerciseDefinition:
    id: str
    learning_unit_id: str
    exercise_type: str
    module_package: str
    position: int
    start: int
    end: int
    target_text: str
    sentence: str
    segments: tuple[PromptSegment, ...]


@dataclass(frozen=True, slots=True)
class ExerciseGeneration:
    id: str
    lesson_id: str
    status: str
    accepted_unit_ids: tuple[str, ...]
    chip_unit_ids: tuple[str, ...]
    created_at: datetime
    definitions: tuple[ExerciseDefinition, ...]


@dataclass(frozen=True, slots=True)
class PassItem:
    position: int
    mode: str
    learning_unit_id: str
    definition_id: str


@dataclass(frozen=True, slots=True)
class PracticeSession:
    id: str
    lesson_id: str
    generation_id: str
    status: str
    cursor: int
    items: tuple[PassItem, ...]


@dataclass(frozen=True, slots=True)
class CurrentItem:
    mode: str
    learning_unit_id: str
    exercise_type: str
    position: int
    start: int
    end: int
    target_text: str
    sentence: str
    segments: tuple[PromptSegment, ...]
    chip_unit_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PracticeView:
    session_id: str
    lesson_id: str
    open: bool
    cursor: int
    current: CurrentItem | None


@dataclass(frozen=True, slots=True)
class Attempt:
    id: str
    session_id: str
    learning_unit_id: str
    span_start: int
    span_end: int
    unit_text: str
    mode: str
    submitted: str
    category: str
    expected: str
    explanation: str
    chunks_used: tuple[str, ...]
    chunks_missed: tuple[str, ...]
    natural_alternative: str | None
    created_at: datetime
