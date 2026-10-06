"""attempt.list_for_lesson — saved attempts with a disposition computed here, not in HTTP."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from lait.application.queries.lesson_get import LessonNotFoundError
from lait.domain.lesson import Lesson
from lait.domain.practice_session import ABANDONED, CLOSED, OPEN, AttemptRecord

QUERY_NAME = "attempt.list_for_lesson"

COMPLETED_PASS = "completed"
EXITED_PASS = "exited"
ABANDONED_PASS = "abandoned"
OPEN_PASS = "open"


@dataclass(frozen=True, slots=True)
class ListedAttempt:
    attempt_id: str
    session_id: str
    session_disposition: str
    mode: str
    category: str
    submitted: str
    expected: str
    explanation: str
    unit_text: str
    span_start: int
    span_end: int
    pass_item_count: int
    created_at: datetime


@dataclass(frozen=True, slots=True)
class AttemptList:
    attempts: tuple[ListedAttempt, ...]


class AttemptListRepository(Protocol):
    def get(self, lesson_id: str) -> Lesson | None: ...

    def list_attempt_records_for_lesson(self, lesson_id: str) -> list[AttemptRecord]: ...


def handle(lesson_id: str, repository: AttemptListRepository) -> AttemptList:
    if repository.get(lesson_id) is None:
        raise LessonNotFoundError(lesson_id)
    rows = repository.list_attempt_records_for_lesson(lesson_id)
    return AttemptList(
        attempts=tuple(
            ListedAttempt(
                attempt_id=row.attempt_id,
                session_id=row.session_id,
                session_disposition=session_disposition(
                    row.session_status, row.cursor, row.session_item_count
                ),
                mode=row.mode,
                category=row.category,
                submitted=row.submitted,
                expected=row.expected,
                explanation=row.explanation,
                unit_text=row.unit_text,
                span_start=row.span_start,
                span_end=row.span_end,
                pass_item_count=row.pass_item_count,
                created_at=row.created_at,
            )
            for row in rows
        )
    )


def session_disposition(status: str, cursor: int, pass_item_count: int) -> str:
    if status == ABANDONED:
        return ABANDONED_PASS
    if status == CLOSED:
        if cursor >= pass_item_count:
            return COMPLETED_PASS
        return EXITED_PASS
    if status == OPEN:
        return OPEN_PASS
    return OPEN_PASS
