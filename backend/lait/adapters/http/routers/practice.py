"""Map practice DTOs onto start, get, submit, finish, and start over."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from lait.application.commands.exercise_submit_attempt import SubmitAttempt
from lait.application.commands.exercise_submit_attempt import handle as submit_attempt
from lait.application.commands.practice_finish import PracticeFinish
from lait.application.commands.practice_finish import handle as finish_practice
from lait.application.commands.practice_start import PracticeStart
from lait.application.commands.practice_start import handle as start_practice
from lait.application.commands.practice_start_over import PracticeStartOver
from lait.application.commands.practice_start_over import handle as start_over_practice
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.application.queries.practice_get import handle as get_practice
from lait.domain.practice_session import (
    CurrentItem,
    NoCurrentItemError,
    PracticeSessionNotFoundError,
    PracticeView,
    StaleGenerationError,
)

router = APIRouter()


class SegmentResponse(BaseModel):
    kind: str
    text: str


class CurrentItemResponse(BaseModel):
    mode: str
    learning_unit_id: str
    exercise_type: str
    position: int
    start: int
    end: int
    target_text: str
    sentence: str
    segments: list[SegmentResponse]
    chip_unit_ids: list[str]


class PracticeResponse(BaseModel):
    session_id: str
    lesson_id: str
    open: bool
    cursor: int
    current: CurrentItemResponse | None


class PracticeStartBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lesson_id: str


class SubmitBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str
    text: str
    submitted_unit_id: str | None = None
    target_learning_unit_id: str | None = None


class SubmitResponse(BaseModel):
    attempt_id: str
    session_open: bool
    cursor: int
    category: str
    submitted: str
    expected: str
    explanation: str
    chunks_used: list[str]
    chunks_missed: list[str]
    natural_alternative: str | None
    learning_unit_id: str
    span_start: int
    span_end: int
    unit_text: str


def _repository(request: Request):
    return request.app.state.lesson_repository


def _registry(request: Request):
    return request.app.state.module_registry


def _current_response(item: CurrentItem) -> CurrentItemResponse:
    return CurrentItemResponse(
        mode=item.mode,
        learning_unit_id=item.learning_unit_id,
        exercise_type=item.exercise_type,
        position=item.position,
        start=item.start,
        end=item.end,
        target_text=item.target_text,
        sentence=item.sentence,
        segments=[
            SegmentResponse(kind=segment.kind, text=segment.text) for segment in item.segments
        ],
        chip_unit_ids=list(item.chip_unit_ids),
    )


def _practice_response(view: PracticeView) -> PracticeResponse:
    return PracticeResponse(
        session_id=view.session_id,
        lesson_id=view.lesson_id,
        open=view.open,
        cursor=view.cursor,
        current=None if view.current is None else _current_response(view.current),
    )


@router.post("/api/practice-sessions", status_code=201, operation_id="practice.start")
def post_practice_session(body: PracticeStartBody, request: Request) -> PracticeResponse:
    repository = _repository(request)
    try:
        view = start_practice(
            PracticeStart(lesson_id=body.lesson_id),
            repository,
            repository,
            _registry(request),
        )
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc
    except StaleGenerationError as exc:
        raise HTTPException(
            status_code=409,
            detail="Generate exercises again before practice",
        ) from exc
    return _practice_response(view)


@router.get("/api/practice-sessions/{session_id}", operation_id="practice.get")
def get_practice_session(session_id: str, request: Request) -> PracticeResponse:
    try:
        view = get_practice(session_id, _repository(request))
    except PracticeSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Practice session not found") from exc
    return _practice_response(view)


@router.post(
    "/api/practice-sessions/{session_id}/attempts",
    operation_id="exercise.submit_attempt",
)
def post_attempt(session_id: str, body: SubmitBody, request: Request) -> SubmitResponse:
    try:
        result = submit_attempt(
            SubmitAttempt(
                session_id=session_id,
                kind=body.kind,
                text=body.text,
                submitted_unit_id=body.submitted_unit_id,
                target_learning_unit_id=body.target_learning_unit_id,
            ),
            _repository(request),
            _registry(request),
        )
    except PracticeSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Practice session not found") from exc
    except NoCurrentItemError as exc:
        raise HTTPException(status_code=409, detail="No current exercise item") from exc
    return SubmitResponse(
        attempt_id=result.attempt_id,
        session_open=result.session_open,
        cursor=result.cursor,
        category=result.category,
        submitted=result.submitted,
        expected=result.expected,
        explanation=result.explanation,
        chunks_used=list(result.chunks_used),
        chunks_missed=list(result.chunks_missed),
        natural_alternative=result.natural_alternative,
        learning_unit_id=result.learning_unit_id,
        span_start=result.span_start,
        span_end=result.span_end,
        unit_text=result.unit_text,
    )


@router.post(
    "/api/practice-sessions/{session_id}/finish",
    operation_id="practice.finish",
)
def post_practice_finish(session_id: str, request: Request) -> PracticeResponse:
    try:
        view = finish_practice(PracticeFinish(session_id=session_id), _repository(request))
    except PracticeSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Practice session not found") from exc
    return _practice_response(view)


@router.post(
    "/api/practice-sessions/{session_id}/start-over",
    operation_id="practice.start_over",
)
def post_practice_start_over(session_id: str, request: Request) -> PracticeResponse:
    repository = _repository(request)
    try:
        view = start_over_practice(
            PracticeStartOver(session_id=session_id),
            repository,
            repository,
            _registry(request),
        )
    except PracticeSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Practice session not found") from exc
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc
    except StaleGenerationError as exc:
        raise HTTPException(
            status_code=409,
            detail="Generate exercises again before practice",
        ) from exc
    return _practice_response(view)
