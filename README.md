# AI Language Coach

Modular, AI-assisted language-learning platform focused on converting passive knowledge into active speech through retrieval practice, lexical chunks, semantic feedback, and spaced repetition.

## Status

Pre-alpha repository skeleton prepared for GSD-driven discovery, architecture, planning, and implementation.

## Architecture direction

- Modular monolith
- Small Core
- Mod-First extension architecture
- Statically bundled trusted modules for MVP
- Public contracts for exercises, languages, AI providers, AI features, schedulers, importers, exporters, and future MCP adapters

## Local lesson loop

Phase 1 application code lives in `backend/` and `frontend/`. HTTP routes map DTOs onto the in-process handlers `lesson.create`, `lesson.list`, and `lesson.get`. There is no account and no language picker.

```powershell
uv sync
uv run alembic -c backend/alembic.ini upgrade head
uv run --python 3.14 python -m uvicorn lait.adapters.http.app:create_app --factory --app-dir backend --host 127.0.0.1 --port 8000
```

```powershell
npm install --prefix frontend
npm run dev --prefix frontend
```

Open `http://127.0.0.1:5173/`. The Vite dev server proxies `/api` and `/health` to port 8000. SQLite defaults to `data/lait.db` (WAL, `busy_timeout`).

## OpenAPI client

HTTP is a DTO adapter over the in-process commands and queries (`lesson.create`, `module_registry.describe`, and the rest of the D-23 names). Regenerate the TypeScript client after a route change:

```powershell
uv run python -m lait.adapters.http.export_openapi
npm run openapi:generate --prefix frontend
```

`frontend/src/api/generated` is committed. CI runs the same export and `openapi:generate`, then `git diff --exit-code -- frontend/src/api/generated`. An interrupted generate leaves that tree dirty; do not commit a partial client. The generator is pinned at `@hey-api/openapi-ts@0.99.0`. The exported document and the client do not contain provider secrets.

## Docker Compose

One command creates a fresh volume, runs Alembic `upgrade head`, and waits until `/health` is HTTP 200. No manual SQLite edits.

```powershell
docker compose up -d --wait
```

- API: `http://127.0.0.1:8000/health` — `{"status":"ok"}` only after migrations
- Web: `http://127.0.0.1:5173/`
- Database: volume `app-data`, file `/app/data/lait.db` (`LAIT_DATABASE_URL` inside the api container)

Copy `.env.example` to `.env` only to change `APP_PORT` or `WEB_PORT`. Compose starts without that file. `docker compose down -v` removes the volume.

## Repository layout

- `backend/` — FastAPI adapter, application handlers, SQLite persistence
- `frontend/` — React lesson list and workspace shell
- `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.web` — Compose stack; build contexts are `backend/` and `frontend/`
- `apps/` — placeholder deployable clients and services (not used by Compose)
- `packages/` — shared SDK, contracts, and UI packages
- `plugins/` — official and future community modules
- `docs/` — PRD, ADRs, research, and architecture documentation
- `docker/` — container-related assets
- `scripts/` — development and maintenance scripts
- `tests/` — cross-cutting and integration tests

## Documentation

- Product requirements: `docs/prd/PRD.md`
- Architecture decisions: `docs/adr/`
- Research: `docs/research/`
- Architecture: `docs/architecture/`
