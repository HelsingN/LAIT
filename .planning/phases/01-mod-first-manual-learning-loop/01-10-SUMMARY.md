---
phase: 01-mod-first-manual-learning-loop
plan: 10
subsystem: infra
tags: [docker, compose, alembic, nginx, sqlite]

requires:
  - phase: 01-01
    provides: walking-skeleton /health and Alembic lessons migration
provides:
  - Compose stack that becomes healthy only after Alembic upgrade head
  - Static frontend image that proxies /api and /health to the api service
  - Documented one-command local start
affects: [01-09]

actuals:
  tokens: 2007
  tasks: 2
  commits: 2

tech-stack:
  added: [python:3.14-slim-bookworm, node:24-bookworm-slim, nginx:1.28-alpine, uv:0.12.21]
  patterns: [migrate-then-exec uvicorn, backend/frontend Compose build contexts, nginx proxy for relative /api]

key-files:
  created:
    - Dockerfile.api
    - Dockerfile.web
    - docker/api_entrypoint.py
    - docker/web-nginx.conf
  modified:
    - docker-compose.yml
    - .env.example
    - README.md

key-decisions:
  - "Compose build contexts are ./backend and ./frontend; uv.lock and the nginx config come from an additional workspace context"
  - "The API entrypoint calls database.migrate (Alembic upgrade head) and only then execs uvicorn, so /health cannot return 200 on an unmigrated volume"
  - "The web image is a Vite production build served by nginx, which proxies /api and /health to the api service"

patterns-established:
  - "Pattern: Compose health is the uvicorn /health probe, and uvicorn does not start until migrate() returns"
  - "Pattern: SQLite for Compose lives on the app-data volume at sqlite:////app/data/lait.db"

requirements-completed: [PLAT-03]

coverage:
  - id: D1
    description: "docker compose up -d --wait reaches a healthy API only after Alembic upgrade head"
    requirement: PLAT-03
    verification:
      - kind: other
        ref: "docker compose up -d --wait && curl.exe http://127.0.0.1:8000/health"
        status: pass
    human_judgment: false
  - id: D2
    description: "A fresh app-data volume reaches healthy without hand-editing SQLite"
    requirement: PLAT-03
    verification:
      - kind: other
        ref: "docker compose down -v && docker compose up -d --wait; alembic_version 20261001_0002"
        status: pass
    human_judgment: false
  - id: D3
    description: "README documents the one-command Compose start"
    requirement: PLAT-03
    verification:
      - kind: other
        ref: "README.md#Docker Compose"
        status: pass
    human_judgment: false

duration: 31min
completed: 2026-10-01
status: complete
plan_head_before: 1dcda492ea07c7871ea22bac0ab64bdf0555e64c
plan_head_after: dfc2f072696ce35d78bf0b3fdaeab02ad43467e9
---

# Phase 1 Plan 10: Compose Migrate-Then-Health Summary

**Docker Compose serves `/health` 200 only after Alembic `upgrade head` on a fresh SQLite volume, with the Vite build proxied through nginx**

## Performance

- **Duration:** 31 min
- **Started:** 2026-10-01T06:25:00Z
- **Completed:** 2026-10-01T06:56:00Z
- **Tasks:** 2
- **Files modified:** 10

## Accomplishments

- `docker compose up -d --wait` on a new `app-data` volume becomes healthy without manual SQLite edits.
- The api container runs `database.migrate` (`upgrade head`) and only then replaces the process with uvicorn. `/health` returned HTTP 200 and `{"status":"ok"}`.
- `alembic_version` on that volume is `20261001_0002`, with `lessons` and `learning_units` present.
- The web container serves the frontend build on port 5173 and proxies `/api` and `/health` to the api service.
- README documents `docker compose up -d --wait`.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end Compose migrate → /health healthy** - `fce33e9` (feat)
2. **Task 2: Compose wait gate + README one-command start** - `dfc2f07` (docs)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `Dockerfile.api` - Python 3.14 image; installs the locked project with uv, then the migrate-then-serve entrypoint
- `Dockerfile.web` - Node 24 build of `frontend/`, nginx 1.28 serves `dist`
- `docker/api_entrypoint.py` - `migrate(LAIT_DATABASE_URL)` then `exec` uvicorn
- `docker/web-nginx.conf` - SPA fallback plus `/api` and `/health` proxy to `api:8000`
- `docker-compose.yml` - build contexts `./backend` and `./frontend`; api healthcheck on `/health`
- `.env.example` - host `LAIT_DATABASE_URL` versus the container volume URL
- `README.md` - one-command Compose start
- `.dockerignore`, `backend/.dockerignore`, `frontend/.dockerignore` - keep host `node_modules` and bytecode out of the image

## Decisions Made

- Build contexts are `./backend` and `./frontend`. `uv.lock`, `pyproject.toml`, and `docker/web-nginx.conf` are copied from an additional `workspace` context so the lockfile stays the install source.
- Readiness is ordering, not a database probe inside `/health`. The 01-01 handler stays a liveness stub. uvicorn is not started until Alembic upgrade head returns.
- The web tier is the production Vite build behind nginx. Relative `/api` fetches from the lesson UI reach the api service without a host-side Vite proxy.

## TDD Gate Compliance

Not applicable. Plan type is `execute`. Neither task sets `tdd="true"` or a `<behavior>` block, so they are not behavior-adding under the MVP+TDD predicate. Task 1 verify is the existing lesson pytest suite (14 passed). Task 2 verify is `docker compose up -d --wait`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Context-local Docker ignore files**
- **Found during:** Task 1 (Compose image build)
- **Issue:** Root `.dockerignore` does not apply to `context: ./frontend`. The first web build sent about 80MB of host `node_modules` and `COPY .` would replace the Linux `npm ci` tree.
- **Fix:** Added `frontend/.dockerignore` and `backend/.dockerignore`, then rebuilt. The web context dropped to about 1KB of source and `npm run build` still succeeded.
- **Files modified:** `frontend/.dockerignore`, `backend/.dockerignore`, `.dockerignore`
- **Verification:** `docker compose build` then `docker compose up -d --wait` exited 0
- **Committed in:** `fce33e9`

**2. [Rule 2 - Missing Critical] nginx proxy for relative `/api`**
- **Found during:** Task 1 (web image)
- **Issue:** The lesson UI fetches `/api/...` on the page origin. A static file server with no proxy cannot reach the api container.
- **Fix:** nginx listens on 5173 and proxies `/api/` and `/health` to `http://api:8000`, re-resolving the Compose DNS name.
- **Files modified:** `docker/web-nginx.conf`, `Dockerfile.web`
- **Verification:** `curl.exe http://127.0.0.1:5173/` returned 200 and `curl.exe http://127.0.0.1:5173/health` returned `{"status":"ok"}`
- **Committed in:** `fce33e9`

---

**Total deviations:** 2 auto-fixed (2 missing critical)
**Impact on plan:** Both keep the walking-skeleton images runnable. Lesson handlers were not changed.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required. Docker Desktop must be running. A `.env` file is optional.

## Next Phase Readiness

Ready for `01-09` to re-run `docker compose up -d --wait` as the full-phase smoke. PLAT-03 stays shared with `01-09`, so the requirement checkbox is not flipped by this plan alone.

## Self-Check: PASSED

- FOUND: `.planning/phases/01-mod-first-manual-learning-loop/01-10-SUMMARY.md`
- FOUND: `fce33e9`
- FOUND: `dfc2f07`
- `main` remains `6d00e33`; commits are on `phase/01-execution`

## Known Stubs

None.

## Authentication Gates

None.

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
