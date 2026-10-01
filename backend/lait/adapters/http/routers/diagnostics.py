"""Map registry DTOs onto describe and list_visible_for. No repository access."""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from lait.application.queries.exercise_registry_list_visible import handle as list_visible_for
from lait.application.queries.module_registry_describe import handle as describe

router = APIRouter()


class ExerciseRegistryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    exercise_type: str
    visibility: str
    module_id: str


class ExerciseRegistryResponse(BaseModel):
    exercises: list[ExerciseRegistryItem]


class ModuleRegistryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    module_id: str
    module_version: str
    category: str
    capabilities: list[str]
    exercise_type: str
    visibility: str
    activation_status: str


class ModuleRegistryResponse(BaseModel):
    modules: list[ModuleRegistryItem]


def _registry(request: Request):
    return request.app.state.module_registry


@router.get("/api/exercise-registry")
def get_exercise_registry(visibility: str, request: Request) -> ExerciseRegistryResponse:
    rows = list_visible_for(visibility, _registry(request))
    return ExerciseRegistryResponse(
        exercises=[
            ExerciseRegistryItem(
                exercise_type=row.exercise_type,
                visibility=row.visibility,
                module_id=row.module_id,
            )
            for row in rows
        ]
    )


@router.get("/api/module-registry")
def get_module_registry(request: Request) -> ModuleRegistryResponse:
    rows = describe(_registry(request))
    return ModuleRegistryResponse(
        modules=[
            ModuleRegistryItem(
                module_id=row.module_id,
                module_version=row.module_version,
                category=row.category,
                capabilities=list(row.capabilities),
                exercise_type=row.exercise_type,
                visibility=row.visibility,
                activation_status=row.activation_status,
            )
            for row in rows
        ]
    )
