---
phase: 01-mod-first-manual-learning-loop
plan: 08
subsystem: api
tags: [openapi, hey-api, fastapi, typescript, ci]

requires:
  - phase: 01-05
    provides: exercise.generate and practice.start HTTP routes
  - phase: 01-07
    provides: lesson feature fetch calls for focus practice
  - phase: 01-10
    provides: practice.finish and practice.start_over routes
provides:
  - OpenAPI 3.1 export via lait.adapters.http.export_openapi
  - Committed TypeScript client at frontend/src/api/generated from @hey-api/openapi-ts 0.99.0
  - CI dirty-diff gate on frontend/src/api/generated
affects: [01-09]

actuals:
  tokens: 34170
  tasks: 3
  commits: 4
plan_head_before: 1275bd555b719f8f253443b92938e11da00c8951
plan_head_after: 0f55d8851ba219963f0e7c6441940bde18a710c1

tech-stack:
  added: ["@hey-api/openapi-ts@0.99.0"]
  patterns:
    - "D-23 command and query names are FastAPI operationIds"
    - "HTTP stays a DTO adapter; the lesson feature calls the generated SDK"
    - "openapi:generate writes in place and does not restore a partial tree"

key-files:
  created:
    - backend/lait/adapters/http/export_openapi.py
    - frontend/openapi-ts.config.ts
    - frontend/scripts/openapi-generate.mjs
    - frontend/src/api/client-config.ts
    - frontend/src/api/generated/sdk.gen.ts
    - .github/workflows/ci.yml
  modified:
    - backend/lait/adapters/http/routers/lessons.py
    - backend/lait/adapters/http/routers/diagnostics.py
    - frontend/src/features/lesson/lessonApi.ts
    - frontend/package.json
    - pyproject.toml

key-decisions:
  - "Pin @hey-api/openapi-ts at exactly 0.99.0 after the legitimacy gate"
  - "operationIds are the D-23 names, including module_registry.describe and practice.start_over"
  - "Install lait as an editable package so uv run python -m lait.adapters.http.export_openapi imports without PYTHONPATH"
  - "The lesson feature keeps its function names and maps 409/422 onto LearningUnitRequestError through the generated SDK"

patterns-established:
  - "Pattern: regenerate with uv run python -m lait.adapters.http.export_openapi then npm run openapi:generate --prefix frontend"
  - "Pattern: CI fails closed on git diff --exit-code -- frontend/src/api/generated"

requirements-completed: [PLAT-09, MODL-12]

coverage:
  - id: D1
    description: "OpenAPI 3.1 operationIds match the D-23 command and query names, including module_registry.describe."
    requirement: PLAT-09
    verification:
      - kind: unit
        ref: "backend/tests/adapters/http/test_openapi_contract.py#test_openapi_operation_ids_match_d23_names"
        status: pass
      - kind: unit
        ref: "backend/tests/adapters/http/test_openapi_contract.py#test_export_openapi_writes_openapi_31_without_secrets"
        status: pass
    human_judgment: false
  - id: D2
    description: "The committed TypeScript client matches a fresh export and generate."
    requirement: PLAT-09
    verification:
      - kind: other
        ref: "uv run python -m lait.adapters.http.export_openapi && npm --prefix frontend run openapi:generate && git diff --exit-code -- frontend/src/api/generated"
        status: pass
    human_judgment: false
  - id: D3
    description: "The lesson feature calls the generated SDK. Frontend tests and the production build pass against those types."
    requirement: MODL-12
    verification:
      - kind: unit
        ref: "npm --prefix frontend test"
        status: pass
      - kind: other
        ref: "npm --prefix frontend run build"
        status: pass
    human_judgment: false
  - id: D4
    description: "CI exports OpenAPI, runs openapi:generate, and fails on a dirty frontend/src/api/generated tree."
    requirement: PLAT-09
    verification:
      - kind: other
        ref: "git grep -n openapi:generate .github/workflows/ci.yml && git grep -n \"git diff --exit-code -- frontend/src/api/generated\" .github/workflows/ci.yml"
        status: pass
    human_judgment: false

duration: 33min
completed: 2026-10-02
status: complete
---

# Phase 1 Plan 08: OpenAPI Client Summary

**Pinned @hey-api/openapi-ts 0.99.0 generates a committed TypeScript client from FastAPI OpenAPI 3.1, and CI fails when that client drifts**

## Performance

- **Duration:** 33 min
- **Started:** 2026-10-02T00:06:00Z
- **Completed:** 2026-10-02T00:38:46Z
- **Tasks:** 3
- **Files modified:** 32

## Accomplishments

- `uv run python -m lait.adapters.http.export_openapi` writes OpenAPI 3.1. Stable operationIds are the D-23 names, including `module_registry.describe`.
- `@hey-api/openapi-ts` is pinned at `0.99.0`. `npm run openapi:generate` writes `frontend/src/api/generated` in place. A second generate leaves `git diff --exit-code -- frontend/src/api/generated` clean.
- `lessonApi.ts` calls the generated SDK. Vitest (33) and `npm run build` pass. The client does not embed provider secrets.
- `.github/workflows/ci.yml` runs pytest, vitest, `docker compose up -d --wait`, export, `openapi:generate`, and the dirty-diff.

## Task Commits

Each task was committed atomically:

1. **Task 1: Legitimacy gate for @hey-api/openapi-ts** - resolved before this executor (`approved 0.99.0`). No commit.
2. **Task 2: End-to-end OpenAPI export → generate → dirty-diff clean** - `806d633` (test, RED) then `fde05a2` (feat, GREEN) then `b640744` (feat, lesson SDK)
3. **Task 3: CI gate for OpenAPI client drift** - `0f55d88` (feat)

## Files Created/Modified

- `backend/lait/adapters/http/export_openapi.py` - writes the OpenAPI 3.1 document
- `backend/lait/adapters/http/routers/lessons.py` - `lesson.create`, `lesson.list`, `lesson.get`
- `backend/lait/adapters/http/routers/diagnostics.py` - `exercise_registry.list_visible_for`, `module_registry.describe`
- `frontend/openapi-ts.config.ts` - generator config for the pinned 0.99.0 CLI
- `frontend/scripts/openapi-generate.mjs` - in-place generate; no tree restore on failure
- `frontend/src/api/generated/` - committed client
- `frontend/src/api/client-config.ts` - same-origin base URL and relative fetch for the existing tests
- `frontend/src/features/lesson/lessonApi.ts` - generated SDK adapter
- `.github/workflows/ci.yml` - dirty-diff gate
- `pyproject.toml` / `uv.lock` - editable `lait` install so the export module imports

## Decisions Made

- Pin exactly `@hey-api/openapi-ts@0.99.0`. Do not float the version.
- Keep fetch relative to the page origin so the Vite proxy and the existing fetch stubs still see `/api/...`.
- Install the backend as an editable package. Docker still starts with `PYTHONPATH=/app/backend` and `--no-install-project`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Editable install so `python -m lait.adapters.http.export_openapi` imports**
- **Found during:** Task 2 (OpenAPI export)
- **Issue:** `uv run python` could not import `lait`. Pytest only adds `backend` via `pythonpath`. The plan's export command has no `PYTHONPATH`.
- **Fix:** Set `[tool.uv] package = true` with hatchling mapping `backend/lait` to `lait`. `uv.lock` changes `source` from `virtual` to `editable`.
- **Files modified:** `pyproject.toml`, `uv.lock`
- **Verification:** `uv run python -c "import lait.adapters.http.export_openapi"` and the export command exit 0
- **Committed in:** `fde05a2`

**2. [Rule 1 - Bug] Generated client called `fetch` with a `Request`, which broke relative URL stubs**
- **Found during:** Task 2 (lesson API)
- **Issue:** `@hey-api/client-fetch` builds `new Request(url)`. jsdom rejects a relative URL, and the lesson tests read `fetch(url, init)` plus exact `url === "/api/practice-sessions"`.
- **Fix:** `client-config.ts` sets `baseUrl` to `location.origin` and re-invokes `globalThis.fetch` with the pathname and search string.
- **Files modified:** `frontend/src/api/client-config.ts`
- **Verification:** `npm --prefix frontend test` — 33 passed
- **Committed in:** `fde05a2`

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** Both were required for the export command and the existing lesson tests. No new transport and no MCP.

## Issues Encountered

Two pytest failures were already red at `1275bd5` and do not touch this plan's behavior:

- `test_lesson_list_ui_locks_copy_and_self_hosted_fonts` expects "Create Lesson" inside `LessonListPage.tsx`. The string is in `CreateLessonForm.tsx`.
- `test_lesson_feature_does_not_call_module_registry_describe` scans test files that mention `/api/module-registry` in negative assertions.

Logged in `deferred-items.md`. The new OpenAPI tests passed. Full pytest otherwise: 82 passed, those 2 failed.

## User Setup Required

None - no external service configuration required.

## Known Stubs

| File | Line | Reason |
|------|------|--------|
| `frontend/src/api/generated/client/client.gen.ts` | 214 | Upstream generator comment `TODO: we probably want to return error and improve types`. Error responses still return `{ error, response }` with `throwOnError: false`. Regenerating would restore the comment. |

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 2 OpenAPI operationIds | `806d633` `RED_EVIDENCE_OK` / `target_test_failed` for `test_openapi_operation_ids_match_d23_names` (exit 1, missing `lesson.create`, `lesson.list`, `lesson.get`, `exercise_registry.list_visible_for`, `module_registry.describe`) | `fde05a2`, `b640744` | — | Pass |

Task 3 is CI config. No behavior block, so no RED commit.

## Threat Flags

None. The export reads no credentials. A scan of `frontend/src/api/generated` and `frontend/openapi.json` found no `sk-`, `api_key`, `secret`, or `password` material. T-01-20 is mitigated by the completed legitimacy gate and the exact `0.99.0` pin.

## Next Phase Readiness

Ready for 01-09. The OpenAPI dirty-diff command is green on this tree. `MODL-12` stays shared with a sibling plan that has no summary yet, so requirements marking completes only `PLAT-09` here.

## Self-Check: PASSED

- FOUND: `backend/lait/adapters/http/export_openapi.py`
- FOUND: `frontend/src/api/generated/sdk.gen.ts`
- FOUND: `.github/workflows/ci.yml`
- FOUND: `806d633`
- FOUND: `fde05a2`
- FOUND: `b640744`
- FOUND: `0f55d88`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-02*
