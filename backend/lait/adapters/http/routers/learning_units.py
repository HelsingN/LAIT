"""Map learning-unit DTOs onto add, remove, accept, and list handlers."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from lait.application.commands.learning_unit_accept import LearningUnitAccept
from lait.application.commands.learning_unit_accept import handle as accept_unit
from lait.application.commands.learning_unit_add import LearningUnitAdd
from lait.application.commands.learning_unit_add import handle as add_unit
from lait.application.commands.learning_unit_remove import LearningUnitRemove
from lait.application.commands.learning_unit_remove import handle as remove_unit
from lait.application.queries.learning_unit_list import handle as list_units
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.domain.learning_unit import (
    LearningUnit,
    LearningUnitNotFoundError,
    MissingSpanError,
    SpanOutOfRangeError,
    SpanOverlapError,
    UnitSetFrozenError,
)

router = APIRouter()


class LearningUnitAddBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: int
    end: int


class LearningUnitResponse(BaseModel):
    id: str
    lesson_id: str
    start: int
    end: int
    text: str
    status: str
    created_at: str
    removed_at: str | None = None


class LearningUnitListResponse(BaseModel):
    learning_units: list[LearningUnitResponse]


def _repositories(request: Request):
    return request.app.state.lesson_repository


def _unit_response(unit: LearningUnit) -> LearningUnitResponse:
    return LearningUnitResponse(
        id=unit.id,
        lesson_id=unit.lesson_id,
        start=unit.start,
        end=unit.end,
        text=unit.text,
        status=unit.status,
        created_at=unit.created_at.isoformat(),
        removed_at=None if unit.removed_at is None else unit.removed_at.isoformat(),
    )


@router.post(
    "/api/lessons/{lesson_id}/learning-units",
    status_code=201,
    operation_id="learning_unit.add",
)
def post_learning_unit(
    lesson_id: str,
    body: LearningUnitAddBody,
    request: Request,
) -> LearningUnitResponse:
    repository = _repositories(request)
    try:
        unit = add_unit(
            LearningUnitAdd(lesson_id=lesson_id, start=body.start, end=body.end),
            repository,
            repository,
        )
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc
    except UnitSetFrozenError as exc:
        raise HTTPException(status_code=409, detail="Learning units are frozen") from exc
    except (MissingSpanError, SpanOutOfRangeError, SpanOverlapError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _unit_response(unit)


@router.post(
    "/api/lessons/{lesson_id}/learning-units/{unit_id}/accept",
    operation_id="learning_unit.accept",
)
def post_accept_learning_unit(
    lesson_id: str,
    unit_id: str,
    request: Request,
) -> LearningUnitResponse:
    repository = _repositories(request)
    try:
        unit = accept_unit(
            LearningUnitAccept(lesson_id=lesson_id, unit_id=unit_id),
            repository,
            repository,
        )
    except UnitSetFrozenError as exc:
        raise HTTPException(status_code=409, detail="Learning units are frozen") from exc
    except LearningUnitNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Learning unit not found") from exc
    return _unit_response(unit)


@router.post(
    "/api/lessons/{lesson_id}/learning-units/{unit_id}/remove",
    operation_id="learning_unit.remove",
)
def post_remove_learning_unit(
    lesson_id: str,
    unit_id: str,
    request: Request,
) -> LearningUnitResponse:
    repository = _repositories(request)
    try:
        unit = remove_unit(
            LearningUnitRemove(lesson_id=lesson_id, unit_id=unit_id),
            repository,
            repository,
        )
    except UnitSetFrozenError as exc:
        raise HTTPException(status_code=409, detail="Learning units are frozen") from exc
    except LearningUnitNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Learning unit not found") from exc
    return _unit_response(unit)


@router.get(
    "/api/lessons/{lesson_id}/learning-units",
    operation_id="learning_unit.list",
)
def get_learning_units(lesson_id: str, request: Request) -> LearningUnitListResponse:
    units = list_units(lesson_id, _repositories(request))
    return LearningUnitListResponse(learning_units=[_unit_response(unit) for unit in units])
