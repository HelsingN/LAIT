"""HTTP composition root. Routers are included as a package, not declared here."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lait.adapters.http.routers import include_routers
from lait.adapters.persistence.database import open_repository
from lait.catalog.loader import load_bundled_catalog
from lait.catalog.validation import parse_catalog_entry, validate_catalog

_DEFAULT_DATABASE_URL = "sqlite:///./data/lait.db"


def create_app(
    database_url: str | None = None,
    *,
    catalog_entries: list[dict] | None = None,
) -> FastAPI:
    if catalog_entries is None:
        modules = load_bundled_catalog()
    else:
        modules = [parse_catalog_entry(entry) for entry in catalog_entries]
    registry = validate_catalog(modules)
    url = database_url or os.environ.get("LAIT_DATABASE_URL", _DEFAULT_DATABASE_URL)
    app = FastAPI(title="AI Language Coach")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
    )
    app.state.module_registry = registry
    app.state.lesson_repository = open_repository(url)
    include_routers(app)
    return app
