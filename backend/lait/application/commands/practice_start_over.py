"""practice.start_over — drop in-progress state, keep Attempts, then start."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime

from lait.application.commands.practice_start import PracticeStart
from lait.application.commands.practice_start import handle as start_practice
from lait.application.ports import LearningUnitRepository, LessonRepository
from lait.catalog.validation import ModuleRecord
from lait.domain.practice_session import (
    ABANDONED,
    OPEN,
    PracticeSessionNotFoundError,
    PracticeView,
    is_open_session,
)

COMMAND_NAME = "practice.start_over"


@dataclass(frozen=True, slots=True)
class PracticeStartOver:
    session_id: str


def handle(
    command: PracticeStartOver,
    lessons: LessonRepository,
    units: LearningUnitRepository,
    registry: Sequence[ModuleRecord],
    *,
    now: Callable[[], datetime] | None = None,
    new_id: Callable[[], str] | None = None,
) -> PracticeView:
    practice = units.get_practice_session(command.session_id)  # type: ignore[attr-defined]
    if practice is None or not is_open_session(practice.status):
        raise PracticeSessionNotFoundError(command.session_id)
    units.set_practice_session_status(command.session_id, ABANDONED)  # type: ignore[attr-defined]
    try:
        return start_practice(
            PracticeStart(lesson_id=practice.lesson_id),
            lessons,
            units,
            registry,
            now=now,
            new_id=new_id,
        )
    except Exception:
        # start writes its session only after its checks pass. Put this session
        # back if that call refuses, so a failed restart does not unfreeze units.
        units.set_practice_session_status(command.session_id, OPEN)  # type: ignore[attr-defined]
        raise
