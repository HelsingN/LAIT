---
phase: 01-mod-first-manual-learning-loop
plan: 01
subsystem: api
tags: [fastapi, sqlite, sqlalchemy, alembic, react, vite]

requires: []
provides:
  - lesson.create, lesson.list, and lesson.get in-process handlers
  - SQLite lessons table with Alembic migration
  - Lesson List and Create Lesson UI on / and /lessons/:id
affects: [01-02, 01-03, 01-10]

actuals:
  tokens: 34495
  tasks: 2
  commits: 2

tech-stack:
  added: [fastapi 0.139.2, pydantic 2.13.5, sqlalchemy 2.0.54, alembic 1.20.0, pytest 9.1.1, react 19.2.8, react-router 8.2.0, vite 8.1.5, typescript 6.0.3, "@tanstack/react-query 5.104.0"]
  patterns: [D-23 handler boundary, HTTP DTO adapter, SQLite WAL busy_timeout, self-hosted WOFF2]

key-files:
  created:
    - backend/lait/application/commands/lesson_create.py
    - backend/lait/application/queries/lesson_list.py
    - backend/lait/application/queries/lesson_get.py
    - backend/lait/adapters/http/app.py
    - frontend/src/features/lesson/LessonListPage.tsx
  modified:
    - README.md

key-decisions:
  - "D-23 handler names are the published application boundary; HTTP only maps DTOs"
  - "Omitted title is suggested from the first meaningful line; a blank title stores Untitled Lesson"
  - "Lesson source max length is 100000 Unicode code points, enforced in the handler and the DTO"
  - "lesson.list orders by created_at descending, then id ascending"
  - "created_at is stored as ISO-8601 text so timezone-aware values round-trip through SQLite"

patterns-established:
  - "Pattern: application handler modules do not import FastAPI or SQLAlchemy"
  - "Pattern: create_app includes routers through adapters/http/routers/include_routers"
  - "Pattern: Source Sans 3 and Source Serif 4 are vendored WOFF2 files, not a font CDN"

requirements-completed: [LESS-01, LESS-02, MODL-12]

coverage:
  - id: D1
    description: "lesson.create persists an exact UTF-8 paste, rejects empty or oversized source, and mints a distinct id per call"
    requirement: LESS-01
    verification:
      - kind: unit
        ref: "backend/tests/application/test_lesson_create.py#test_lesson_create_persists_exact_utf8_source"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_create.py#test_whitespace_only_source_writes_no_row"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_create.py#test_same_paste_twice_creates_distinct_immutable_ids"
        status: pass
    human_judgment: false
  - id: D2
    description: "lesson.list and lesson.get round-trip stored lessons, ordered by created_at descending then id"
    requirement: LESS-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_lesson_list.py#test_lesson_list_and_get_round_trip"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_create.py#test_list_orders_by_created_at_desc_then_id"
        status: pass
    human_judgment: false
  - id: D3
    description: "HTTP POST/GET map DTOs onto the handlers and do not call the persistence package"
    requirement: MODL-12
    verification:
      - kind: integration
        ref: "backend/tests/application/test_lesson_create.py#test_http_maps_create_dto_and_rejects_empty_source"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_list.py#test_http_routers_delegate_to_handlers_not_repositories"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_create.py#test_application_handlers_do_not_import_fastapi_or_sqlalchemy"
        status: pass
    human_judgment: false
  - id: D4
    description: "Lesson List shows the empty state, Create Lesson, and an open link to /lessons/:id"
    requirement: LESS-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_lesson_list.py#test_lesson_list_ui_locks_copy_and_self_hosted_fonts"
        status: pass
    human_judgment: true
    rationale: "Locked copy and font files are asserted in pytest. The paste, list, and open interaction was exercised in the browser during execution and is not a committed browser test."

duration: 18min
completed: 2026-10-01
status: complete
plan_head_before: 6d00e33be532e8137c46e1f995f6ebcc61a74058
plan_head_after: baaec4296f2d98081c66040c982ffa643ac19a8b
---

# Phase 1 Plan 01: Lesson Create and List Summary

**SQLite `lesson.create` / `lesson.list` / `lesson.get` behind D-23 handlers, with a Create Lesson screen and self-hosted Source Sans 3 and Source Serif 4**

## Performance

- **Duration:** 18 min
- **Started:** 2026-10-01T04:32:46Z
- **Completed:** 2026-10-01T04:50:51Z
- **Tasks:** 2
- **Files modified:** 53

## Accomplishments

- A learner can paste English source, store it unchanged, and get a distinct immutable lesson id with no account and no language picker.
- `lesson.list` and `lesson.get` read those rows back. HTTP routers only map DTOs onto the handlers.
- `/` shows No lessons yet, Create Lesson, and Loading… / Creating…. Opening a row goes to `/lessons/:id` and shows the title plus read-only source.

## Task Commits

Each task was committed atomically:

1. **Task 1: Confirm D-23 one-way application boundary** - decision only (`proceed-d23`), no commit
2. **Task 2: End-to-end lesson.create → list → Lesson List UI** - `907d5d8` (test, RED) then `baaec42` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/domain/lesson.py` - immutable lesson, title suggestion, source bounds
- `backend/lait/application/commands/lesson_create.py` - `lesson.create`
- `backend/lait/application/queries/lesson_list.py` - `lesson.list`
- `backend/lait/application/queries/lesson_get.py` - `lesson.get`
- `backend/lait/adapters/persistence/` - SQLAlchemy repository, WAL pragmas, Alembic `lessons` table
- `backend/lait/adapters/http/` - FastAPI composition root and DTO routers
- `frontend/src/features/lesson/LessonListPage.tsx` - Create Lesson and the lesson list
- `frontend/src/features/lesson/LessonWorkspacePage.tsx` - title and read-only source shell
- `frontend/src/fonts/` - vendored Source Sans 3 and Source Serif 4 WOFF2 plus OFL licenses
- `README.md` - local migrate, API, and Vite commands

## Decisions Made

- Confirmed D-23: handler names are the application boundary. No MCP and no distributed bus.
- `title is None` suggests a title from the first meaningful line (markdown heading markers stripped). A blank title stores `Untitled Lesson`.
- Source longer than 100000 code points is rejected and writes no row.
- List order is `created_at` descending, then `id` ascending. Timestamps are ISO-8601 strings so SQLite does not drop the timezone.

## TDD Gate Compliance

| Gate | Commit | Result |
|------|--------|--------|
| RED | `907d5d8` `test(01-01): add failing test for lesson create and list` | `RED_EVIDENCE_OK` / `target_test_failed` for `test_lesson_create_persists_exact_utf8_source` (exit 1, 14 failed) |
| GREEN | `baaec42` `feat(01-01): implement lesson create, list, and Lesson List UI` | 14 passed |
| REFACTOR | — | not needed |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Root tsconfig so `tsc -b` runs from the repo root**
- **Found during:** Task 2 (Lesson List UI)
- **Issue:** `npx --prefix frontend tsc -b --pretty false` keeps the repo root as cwd and looked for `tsconfig.json` there.
- **Fix:** Added a root solution that references `frontend/`.
- **Files modified:** `tsconfig.json`
- **Verification:** the acceptance command exits 0
- **Committed in:** `baaec42`

**2. [Rule 1 - Bug] Alembic CLI creates the SQLite parent directory**
- **Found during:** Task 2 (local migrate)
- **Issue:** `uv run alembic -c backend/alembic.ini upgrade head` failed with `unable to open database file` because `data/` did not exist.
- **Fix:** `backend/alembic/env.py` creates the parent directory for file SQLite URLs before connecting.
- **Files modified:** `backend/alembic/env.py`
- **Verification:** `alembic upgrade head` exits 0 and `/health` returns `{"status":"ok"}`
- **Committed in:** `baaec42`

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** Both fixes make the documented commands runnable. Handler and UI scope did not change.

## Issues Encountered

- Starlette's `TestClient` warns that `httpx` is deprecated in favor of `httpx2`. The suite still passes. `httpx2` is not in STACK.md, so the tests stay on the installed TestClient.
- `react-router@8.2.0` declares `node >= 22.22.0`. This machine has Node 22.17.1. npm printed `EBADENGINE`; `tsc -b` and the Vite dev server still ran.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for `01-02` (static catalog and diagnostic queries). Compose health remains plan `01-10`. `create_app` includes routers through `include_routers`, so later router modules can register without rewriting the composition root except for catalog startup.

## Self-Check: PASSED

- FOUND: `.planning/phases/01-mod-first-manual-learning-loop/01-01-SUMMARY.md`
- FOUND: `907d5d8`
- FOUND: `baaec42`
- `main` remains `6d00e33`; commits are on `phase/01-execution`

## Known Stubs

None.

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
