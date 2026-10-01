"""Map exercise DTOs onto exercise.generate. No repository queries here."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from lait.application.commands.exercise_generate import ExerciseGenerate
from lait.application.commands.exercise_generate import handle as generate_exercises
from lait.application.queries.lesson_get import LessonNotFoundError

router = APIRouter()


class GenerationResponse(BaseModel):
    id: str
    lesson_id: str
    status: str
    accepted_unit_ids: list[str]
    definition_count: int


def _repository(request: Request):
    return request.app.state.lesson_repository


def _registry(request: Request):
    return request.app.state.module_registry


@router.post(
    "/api/lessons/{lesson_id}/exercises/generate",
    operation_id="exercise.generate",
)
def post_generate_exercises(lesson_id: str, request: Request) -> GenerationResponse:
    try:
        outcome = generate_exercises(
            ExerciseGenerate(lesson_id=lesson_id),
            _repository(request),
            _repository(request),
            _registry(request),
        )
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc
    return GenerationResponse(
        id=outcome.id,
        lesson_id=outcome.lesson_id,
        status=outcome.status,
        accepted_unit_ids=list(outcome.accepted_unit_ids),
        definition_count=outcome.definition_count,
    )
