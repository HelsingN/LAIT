---
phase: 01-mod-first-manual-learning-loop
plan: 09
subsystem: testing
tags: [pytest, catalog, fastapi, compose, modl-03, plat-10]

requires:
  - phase: 01-08
    provides: OpenAPI export and committed client dirty-diff
  - phase: 01-10
    provides: Compose stack that is healthy only after Alembic upgrade head
provides:
  - Proof catalog removal test that leaves Gap Fill generating with zero Core or application edits
  - AST isolation guard for application handlers and application tests
  - Independent pytest targets for domain, persistence, modules, and application
affects: [phase-01-verification]

actuals:
  tokens: 10688
  tasks: 3
  commits: 5
plan_head_before: acb360ae835b12392f62278d132d58c54c4e6bc9
plan_head_after: 7d54659bcef374408d71b7e2b842b33097cdf457

tech-stack:
  added: []
  patterns:
    - "Proof removal is a temporary manifest overlay; the shipped catalog still includes proof"
    - "HTTP DTO tests live under backend/tests/adapters/http; application tests do not import the FastAPI app"
    - "An empty pytest directory fails collection; suites do not depend on cross-suite order"

key-files:
  created:
    - backend/tests/catalog/test_proof_removal.py
    - backend/tests/application/test_handler_isolation.py
    - backend/tests/adapters/persistence/test_lesson_repository.py
    - backend/tests/adapters/http/test_http_dto_mapping.py
  modified:
    - README.md
    - .github/workflows/ci.yml
    - backend/tests/application/test_lesson_create.py
    - backend/tests/application/test_learning_unit_add.py
    - backend/tests/application/test_submit_attempt.py
    - backend/tests/application/test_practice_finish_and_start_over.py

key-decisions:
  - "Maintainer removal is delete backend/lait/modules/exercise_proof/manifest.json and the ProofRenderer registration in frontend/src/registries/renderers/registry.ts only"
  - "The acceptance test copies manifests into a temp overlay and monkeypatches bundled_manifest_paths; Core domain and application files are not edited"
  - "Application handler tests must not import fastapi, lait.adapters.http.app, or lait.adapters.persistence.models; HTTP mapping tests moved to the HTTP adapter suite"
  - "CI runs the domain/persistence/modules split and the application suite, and still runs uv run pytest -q plus Compose and the OpenAPI dirty-diff"

patterns-established:
  - "Pattern: proof removal overlay never deletes the shipped exercise_proof manifest"
  - "Pattern: pytest backend/tests/domain, backend/tests/adapters/persistence, backend/tests/modules, and backend/tests/application are separate invocations"

requirements-completed: [PLAT-10, MODL-03, MODL-12, PLAT-03]

coverage:
  - id: D1
    description: "Removing the proof catalog entry leaves the app up, omits proof from describe, still lists Gap Fill, and generates from an accepted unit, with Core and application digests unchanged."
    requirement: MODL-03
    verification:
      - kind: unit
        ref: "backend/tests/catalog/test_proof_removal.py#test_proof_removal"
        status: pass
    human_judgment: false
  - id: D2
    description: "Application handlers and application tests do not import FastAPI or SQLAlchemy table modules. HTTP DTO tests live under the HTTP adapter suite."
    requirement: MODL-12
    verification:
      - kind: unit
        ref: "backend/tests/application/test_handler_isolation.py#test_handler_isolation"
        status: pass
    human_judgment: false
  - id: D3
    description: "Domain, persistence, and module suites collect and pass on their own. An empty directory fails pytest collection."
    requirement: PLAT-10
    verification:
      - kind: unit
        ref: "uv run pytest backend/tests/domain backend/tests/adapters/persistence backend/tests/modules backend/tests/application/test_handler_isolation.py -q"
        status: pass
    human_judgment: false
  - id: D4
    description: "Full phase pytest gate is green."
    requirement: PLAT-10
    verification:
      - kind: unit
        ref: "uv run pytest -q"
        status: pass
    human_judgment: false
  - id: D5
    description: "docker compose up -d --wait reaches healthy api and web containers."
    requirement: PLAT-03
    verification:
      - kind: other
        ref: "docker compose up -d --wait"
        status: pass
    human_judgment: false
  - id: D6
    description: "OpenAPI export and generate leave frontend/src/api/generated clean."
    verification:
      - kind: other
        ref: "uv run python -m lait.adapters.http.export_openapi && npm run openapi:generate --prefix frontend && git diff --exit-code -- frontend/src/api/generated"
        status: pass
    human_judgment: false

duration: 12min
completed: 2026-10-02
status: complete
---

# Phase 1 Plan 09: Independent Suites and Proof Removal Summary

**A temp catalog overlay drops the proof manifest without Core edits, Gap Fill still generates, and domain, persistence, modules, and application pytest suites run as separate commands**

## Performance

- **Duration:** 12 min
- **Started:** 2026-10-02T00:46:09Z
- **Completed:** 2026-10-02T00:58:17Z
- **Tasks:** 3
- **Files modified:** 13

## Accomplishments

- `test_proof_removal` builds a temp manifest overlay without `exercise_proof`, starts the app, omits proof from `module_registry.describe`, returns Gap Fill from `list_visible_for("learner")`, and completes `exercise.generate`. Domain and application file digests do not change. The shipped proof manifest stays on disk.
- README tells a maintainer to delete `backend/lait/modules/exercise_proof/manifest.json` and the `ProofRenderer` registration in `frontend/src/registries/renderers/registry.ts` only.
- `test_handler_isolation` AST-scans application handlers and application tests for `fastapi`, `sqlalchemy`, `lait.adapters.http.app`, and `lait.adapters.persistence.models`. HTTP DTO tests moved to `backend/tests/adapters/http/test_http_dto_mapping.py`.
- Persistence has its own suite (`test_repository_persists_lesson_source`) that does not start FastAPI. CI invokes the domain/persistence/modules split and the application suite separately. An empty directory fails collection.
- Phase gate: `uv run pytest -q` (87 passed), `docker compose up -d --wait` (api and web healthy), OpenAPI dirty-diff clean. `nyquist_compliant` was not flipped.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end proof catalog removal leaves Gap Fill working** - `811e581` (test, RED) then `56a37ad` (feat, GREEN)
2. **Task 2: Expand independent suite partitions + handler isolation** - `1b53208` (test, RED) then `3e26eb3` (feat, GREEN)
3. **Task 3: Full phase smoke: pytest + compose** - `7d54659` (fix)

## Files Created/Modified

- `backend/tests/catalog/test_proof_removal.py` - overlay removal acceptance test
- `README.md` - maintainer removal steps and separate verify commands
- `backend/tests/application/test_handler_isolation.py` - AST import guard and empty-suite backstop
- `backend/tests/adapters/persistence/test_lesson_repository.py` - persistence round-trip without HTTP
- `backend/tests/adapters/http/test_http_dto_mapping.py` - HTTP DTO tests moved out of the application suite
- `.github/workflows/ci.yml` - split pytest steps plus the existing full gate
- `backend/tests/application/test_lesson_list.py` - list copy lock includes `CreateLessonForm.tsx`
- `backend/tests/catalog/test_list_visible_for.py` - describe scan skips lesson `*.test.ts(x)` files

## Decisions Made

- Proof removal in tests is a temp overlay via `bundled_manifest_paths`. The default catalog still includes proof so `module_registry.describe` can show it (T-01-22).
- Maintainer steps are two deletions: the proof `manifest.json` and the frontend `ProofRenderer` registration. No Core or application edits.
- Application tests do not import the FastAPI app. HTTP mapping coverage stays, under `backend/tests/adapters/http`.
- CI keeps `uv run pytest -q`, Compose wait, and the OpenAPI dirty-diff, and adds the PLAT-10 split invocations.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] HTTP DTO tests left the application suite**
- **Found during:** Task 2 (handler isolation)
- **Issue:** Application tests imported `fastapi` and `lait.adapters.http.app`, which MODL-12 forbids for handler tests.
- **Fix:** Moved the four HTTP mapping tests to `backend/tests/adapters/http/test_http_dto_mapping.py` and dropped those imports from the application suite.
- **Files modified:** `backend/tests/application/test_lesson_create.py`, `test_learning_unit_add.py`, `test_submit_attempt.py`, `test_practice_finish_and_start_over.py`, `backend/tests/adapters/http/test_http_dto_mapping.py`
- **Verification:** `uv run pytest backend/tests/application/test_handler_isolation.py backend/tests/adapters/http/test_http_dto_mapping.py -q`
- **Committed in:** `3e26eb3`

**2. [Rule 1 - Bug] Lesson list copy lock looked only at LessonListPage.tsx**
- **Found during:** Task 3 (full pytest)
- **Issue:** `Create Lesson`, `Creating…`, and the create-error string live in `CreateLessonForm.tsx`, which the list page renders. The assertion failed before this plan.
- **Fix:** The lock reads `LessonListPage.tsx` and `CreateLessonForm.tsx`.
- **Files modified:** `backend/tests/application/test_lesson_list.py`
- **Verification:** `test_lesson_list_ui_locks_copy_and_self_hosted_fonts` passed inside `uv run pytest -q`
- **Committed in:** `7d54659`

**3. [Rule 1 - Bug] Describe scan treated negative test assertions as feature calls**
- **Found during:** Task 3 (full pytest)
- **Issue:** `test_lesson_feature_does_not_call_module_registry_describe` read `*.test.tsx` files that mention `/api/module-registry` only to assert it is absent.
- **Fix:** Skip `*.test.ts` and `*.test.tsx` under `frontend/src/features/lesson`. Production sources still must not contain those strings.
- **Files modified:** `backend/tests/catalog/test_list_visible_for.py`
- **Verification:** `test_lesson_feature_does_not_call_module_registry_describe` passed inside `uv run pytest -q`
- **Committed in:** `7d54659`

---

**Total deviations:** 3 auto-fixed (1 missing critical, 2 bugs)
**Impact on plan:** The HTTP move is the MODL-12 test boundary. The two assertion fixes make the phase pytest gate green. No new features, no MCP, no AI.

## Issues Encountered

None. The two pytest failures already logged in `deferred-items.md` were fixed in Task 3 and marked resolved.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 Proof removal | `811e581` `RED_EVIDENCE_OK` / `target_test_failed` for `test_proof_removal` (exit 1, README missing `## Removing the proof exercise`) | `56a37ad` | — | Pass |
| 2 Handler isolation | `1b53208` `RED_EVIDENCE_OK` / `target_test_failed` for `test_handler_isolation` (exit 1, application tests import `fastapi.testclient`) | `3e26eb3` | — | Pass |

Task 3 has no `<behavior>` block. No RED commit.

## Authentication Gates

None.

## Threat Flags

None. The overlay catalog is created under pytest `tmp_path` and is not the shipped catalog. No new endpoints, credentials, or schema changes.

## Next Phase Readiness

Phase 1 plan 09 is complete. `uv run pytest -q` is 87 passed. Compose wait is healthy. OpenAPI `frontend/src/api/generated` is clean. `nyquist_compliant` stays false. Ready for `/gsd-verify-work`.

## Self-Check: PASSED

- FOUND: `backend/tests/catalog/test_proof_removal.py`
- FOUND: `backend/tests/application/test_handler_isolation.py`
- FOUND: `backend/tests/adapters/persistence/test_lesson_repository.py`
- FOUND: `README.md`
- FOUND: `.github/workflows/ci.yml`
- FOUND: `811e581`
- FOUND: `56a37ad`
- FOUND: `1b53208`
- FOUND: `3e26eb3`
- FOUND: `7d54659`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-02*
