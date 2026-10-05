"""exercise.latest_completed and attempt.list_for_lesson over a port fake."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from lait.application.queries.attempt_list_for_lesson import QUERY_NAME as ATTEMPT_QUERY
from lait.application.queries.attempt_list_for_lesson import handle as list_attempts
from lait.application.queries.exercise_latest_completed import QUERY_NAME as LATEST_QUERY
from lait.application.queries.exercise_latest_completed import handle as latest_completed
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.domain.learning_unit import ACCEPTED, DRAFT, LearningUnit
from lait.domain.lesson import Lesson
from lait.domain.practice_session import (
    ABANDONED,
    CLOSED,
    COMPLETED,
    OPEN,
    AttemptRecord,
    ExerciseGeneration,
)

LESSON_ID = "lesson-1"
WHEN = datetime(2026, 10, 2, tzinfo=UTC)


def _lesson() -> Lesson:
    return Lesson(id=LESSON_ID, title="Notes", source="alpha", created_at=WHEN)


def _unit(unit_id: str, status: str = ACCEPTED, removed_at: datetime | None = None) -> LearningUnit:
    return LearningUnit(
        id=unit_id,
        lesson_id=LESSON_ID,
        start=0,
        end=1,
        text=unit_id,
        status=status,
        created_at=WHEN,
        removed_at=removed_at,
    )


def _generation(generation_id: str, accepted: tuple[str, ...]) -> ExerciseGeneration:
    return ExerciseGeneration(
        id=generation_id,
        lesson_id=LESSON_ID,
        status=COMPLETED,
        accepted_unit_ids=accepted,
        chip_unit_ids=accepted,
        created_at=WHEN,
        definitions=(),
    )


def _record(
    attempt_id: str,
    session_id: str,
    status: str,
    cursor: int,
    pass_item_count: int,
    mode: str,
) -> AttemptRecord:
    return AttemptRecord(
        attempt_id=attempt_id,
        session_id=session_id,
        session_status=status,
        cursor=cursor,
        pass_item_count=pass_item_count,
        mode=mode,
        category="correct",
        submitted="alpha",
        expected="alpha",
        explanation="matched",
        unit_text="alpha",
        span_start=0,
        span_end=5,
        created_at=WHEN,
    )


class _Repository:
    def __init__(
        self,
        *,
        present: bool = True,
        units: list[LearningUnit] | None = None,
        generation: ExerciseGeneration | None = None,
        records: list[AttemptRecord] | None = None,
    ) -> None:
        self._lesson = _lesson() if present else None
        self.units = units or []
        self.generation = generation
        self.records = records or []

    def get(self, lesson_id: str) -> Lesson | None:
        if self._lesson is None or self._lesson.id != lesson_id:
            return None
        return self._lesson

    def list_units(self, lesson_id: str) -> list[LearningUnit]:
        return [unit for unit in self.units if unit.lesson_id == lesson_id]

    def latest_completed_generation(self, lesson_id: str) -> ExerciseGeneration | None:
        if self.generation is None or self.generation.lesson_id != lesson_id:
            return None
        return self.generation

    def list_attempt_records_for_lesson(self, lesson_id: str) -> list[AttemptRecord]:
        del lesson_id
        return list(self.records)


def test_matching_generation_is_restorable() -> None:
    repository = _Repository(
        units=[_unit("unit-b"), _unit("unit-a")],
        generation=_generation("generation-1", ("unit-b", "unit-a")),
    )

    result = latest_completed(LESSON_ID, repository)

    assert LATEST_QUERY == "exercise.latest_completed"
    assert result.restorable is True
    assert result.generation_id == "generation-1"
    assert result.accepted_unit_ids == ("unit-b", "unit-a")


def test_mismatched_generation_hides_the_stale_id() -> None:
    repository = _Repository(
        units=[_unit("unit-live")],
        generation=_generation("stale-gen", ("unit-old",)),
    )

    result = latest_completed(LESSON_ID, repository)

    assert result.restorable is False
    assert result.generation_id is None
    assert result.accepted_unit_ids == ()
    assert "stale-gen" not in (result.generation_id or "")


def test_removed_or_draft_units_do_not_count_as_the_accepted_set() -> None:
    repository = _Repository(
        units=[
            _unit("unit-live"),
            _unit("unit-gone", removed_at=WHEN),
            _unit("unit-draft", status=DRAFT),
        ],
        generation=_generation("generation-1", ("unit-live", "unit-gone")),
    )

    result = latest_completed(LESSON_ID, repository)

    assert result.restorable is False
    assert result.generation_id is None


def test_missing_generation_is_not_restorable() -> None:
    repository = _Repository(units=[_unit("unit-live")], generation=None)

    result = latest_completed(LESSON_ID, repository)

    assert result.restorable is False
    assert result.generation_id is None
    assert result.accepted_unit_ids == ()


def test_unknown_lesson_is_not_found_for_both_reads() -> None:
    repository = _Repository(present=False)

    with pytest.raises(LessonNotFoundError):
        latest_completed("missing", repository)
    with pytest.raises(LessonNotFoundError):
        list_attempts("missing", repository)


def test_dispositions_follow_session_status_and_cursor() -> None:
    repository = _Repository(
        records=[
            _record(
                "attempt-done", "session-done", CLOSED, cursor=2, pass_item_count=2, mode="drag"
            ),
            _record(
                "attempt-early", "session-early", CLOSED, cursor=1, pass_item_count=2, mode="typed"
            ),
            _record(
                "attempt-left", "session-left", ABANDONED, cursor=0, pass_item_count=2, mode="drag"
            ),
            _record(
                "attempt-open", "session-open", OPEN, cursor=0, pass_item_count=2, mode="typed"
            ),
        ]
    )

    result = list_attempts(LESSON_ID, repository)

    assert ATTEMPT_QUERY == "attempt.list_for_lesson"
    assert [
        (row.session_id, row.session_disposition, row.mode) for row in result.attempts
    ] == [
        ("session-done", "completed", "drag"),
        ("session-early", "exited", "typed"),
        ("session-left", "abandoned", "drag"),
        ("session-open", "open", "typed"),
    ]


def test_known_lesson_with_no_attempts_returns_an_empty_list() -> None:
    result = list_attempts(LESSON_ID, _Repository())

    assert result.attempts == ()
