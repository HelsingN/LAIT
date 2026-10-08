"""Aggregate HTTP routers so later plans add modules here, not in app.py."""

from __future__ import annotations

from fastapi import FastAPI

from lait.adapters.http.routers.diagnostics import router as diagnostics_router
from lait.adapters.http.routers.exercises import router as exercises_router
from lait.adapters.http.routers.health import router as health_router
from lait.adapters.http.routers.learning_units import router as learning_units_router
from lait.adapters.http.routers.lessons import router as lessons_router
from lait.adapters.http.routers.practice import router as practice_router


def include_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(lessons_router)
    app.include_router(learning_units_router)
    app.include_router(exercises_router)
    app.include_router(practice_router)
    app.include_router(diagnostics_router)
