"""Map lesson DTOs onto lesson.create, lesson.list, and lesson.get."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from lait.application.commands.lesson_create import LessonCreate
from lait.application.commands.lesson_create import handle as create_lesson
from lait.application.queries.lesson_get import LessonNotFoundError
from lait.application.queries.lesson_get import handle as get_lesson
from lait.application.queries.lesson_list import handle as list_lessons
from lait.domain.lesson import (
    MAX_SOURCE_LENGTH,
    MAX_TITLE_LENGTH,
    EmptyLessonSourceError,
    Lesson,
    LessonSourceTooLongError,
    LessonTitleTooLongError,
)

router = APIRouter()


class LessonCreateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1, max_length=MAX_SOURCE_LENGTH)
    title: str | None = Field(default=None, max_length=MAX_TITLE_LENGTH)


class LessonResponse(BaseModel):
    id: str
    title: str
    source: str
    created_at: str


class LessonListResponse(BaseModel):
    lessons: list[LessonResponse]


def _repository(request: Request):
    return request.app.state.lesson_repository


def _lesson_response(lesson: Lesson) -> LessonResponse:
    return LessonResponse(
        id=lesson.id,
        title=lesson.title,
        source=lesson.source,
        created_at=lesson.created_at.isoformat(),
    )


@router.post("/api/lessons", status_code=201)
def post_lesson(body: LessonCreateBody, request: Request) -> LessonResponse:
    try:
        lesson = create_lesson(
            LessonCreate(source=body.source, title=body.title),
            _repository(request),
        )
    except (EmptyLessonSourceError, LessonSourceTooLongError, LessonTitleTooLongError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _lesson_response(lesson)


@router.get("/api/lessons")
def get_lessons(request: Request) -> LessonListResponse:
    lessons = list_lessons(_repository(request))
    return LessonListResponse(lessons=[_lesson_response(lesson) for lesson in lessons])


@router.get("/api/lessons/{lesson_id}")
def get_lesson_by_id(lesson_id: str, request: Request) -> LessonResponse:
    try:
        lesson = get_lesson(lesson_id, _repository(request))
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc
    return _lesson_response(lesson)
