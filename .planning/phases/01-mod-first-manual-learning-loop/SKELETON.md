# Walking Skeleton — AI Language Coach

**Phase:** 1
**Generated:** 2026-09-29

## Capability Proven End-to-End

A learner can paste English source into a new lesson, persist it through `lesson.create`, reopen it from the Lesson List via `lesson.list`/`lesson.get`, and reach a health-checked Docker Compose stack — the first real step on the Gap Fill learner path (later plans expand units → generate → practice → feedback on this same stack).

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Backend layout | `backend/lait/` package; root `pyproject.toml` + `uv.lock` | Matches RESEARCH handler/module layout; `uv run pytest -q` from repo root |
| Frontend layout | `frontend/` Vite 8 + React 19 SPA | Matches RESEARCH/VALIDATION OpenAPI client path `frontend/src/api/generated` |
| HTTP adapter | FastAPI 0.139.x routers map DTOs only | D-23 / ADR-014 — handlers are the application boundary |
| Application boundary | In-process typed command/query handlers named in D-23 | No command bus; no MCP in Phase 1 |
| Data layer | SQLAlchemy 2.0 + Alembic + SQLite WAL | STACK.md; Compose runs migrations before ready |
| Auth | None — single local learner | LESS-01; no login |
| Module catalog | Static build-time manifests; startup validation | MODL-01; Gap Fill `visibility: learner`, proof `visibility: maintainer` (D-21) |
| Exercise generate status | Persist only `completed` \| `failed` in the command transaction | RESEARCH open Q2 + UI-SPEC "Generating…" = client pending |
| OpenAPI TS client | Pin `@hey-api/openapi-ts` | Full typed client; legitimacy gate before install (ASSUMED) |
| Deployment target | Local Docker Compose (`docker-compose.yml`) | PLAT-03; health only after Alembic |
| Directory layout | Hexagonal: `application/`, `domain/`, `adapters/{http,persistence}/`, `modules/`, `catalog/`; frontend `features/lesson`, `registries/renderers` | RESEARCH architecture map |
| Legacy placeholders | Replace empty `apps/api` / `apps/web` Compose targets with `backend` / `frontend` | Existing READMEs are stubs; RESEARCH paths win |

## Stack Touched in Phase 1

- [ ] Project scaffold (framework, build, lint, test runner)
- [ ] Routing — at least one real route (`/` Lesson List, `/lessons/:id` workspace)
- [ ] Database — at least one real read AND one real write (`lesson.create` / `lesson.list`)
- [ ] UI — at least one interactive element wired to the API (Create Lesson → list row)
- [ ] Deployment — `docker compose up -d --wait` reaches healthy after migrations

## Out of Scope (Deferred to Later Slices)

- LLM learning-unit generation (Phase 2)
- Unit-text edit after capture (ANLY-06 / Phase 2)
- Chunk Completion, Sentence Reconstruction, Keyword Recall
- Retry, reveal, session resume
- Full English normalization (EVAL-02 / Phase 3)
- Maintainer diagnostics page (query only in Phase 1)
- MCP adapter (ADR-014)
- Playwright browser projects (PLAT-11 / Phase 9)
- `visibility: experimental` live value

## Subsequent Slice Plan

Each later phase adds one vertical slice on top of this skeleton without altering its architectural decisions:

- Phase 2: AI-assisted learning-unit review over durable jobs
- Phase 3: Chunk Completion + English normalization module
- Phase 4: Sentence Reconstruction + session resume
- Phase 5: Keyword Recall + semantic evaluation
- Phase 6: Weak-unit review scheduler loop
- Phase 7: Lesson lifecycle (rename/archive/delete/re-analyze)
- Phase 8: Public contract parity suite
- Phase 9: Responsive release hardening + Playwright

## Plan Decisions Locked Here

1. **Generate status (EXER-01):** Server persists only terminal `completed` or `failed` inside `exercise.generate`'s transaction. UI shows locked copy "Generating…" while the TanStack mutation is pending; after return, UI reads the stored terminal status. No persisted `queued`/`running` in Phase 1.
2. **Start-over (D-10/D-19):** Application command `practice.start_over` abandons in-progress non-attempt state, then calls `practice.start` on the same frozen accepted set. HTTP only maps the DTO onto that command. Do not overload `practice.finish`. Do not put the orchestration in the router.
3. **OpenAPI generator:** `@hey-api/openapi-ts` pinned in `frontend/package.json`; scripts `openapi:export` (backend) + `openapi:generate` (frontend); CI fails on `git diff --exit-code -- frontend/src/api/generated`.
