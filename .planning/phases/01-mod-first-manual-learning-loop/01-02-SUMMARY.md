---
phase: 01-mod-first-manual-learning-loop
plan: 02
subsystem: api
tags: [fastapi, pydantic, catalog, module-registry, visibility]

requires:
  - phase: 01-01
    provides: create_app composition root and D-23 handler boundary
provides:
  - startup catalog validation that refuses invalid bundled manifests
  - module_registry.describe public metadata query
  - exercise_registry.list_visible_for visibility filter
  - Gap Fill learner contribution and proof maintainer contribution
affects: [01-04, 01-07, 01-09]

actuals:
  tokens: 8154
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns:
    - D-21 visibility on exercise contributions only
    - catalog validated once in create_app before the process serves
    - HTTP diagnostics map DTOs onto registry queries

key-files:
  created:
    - backend/lait/catalog/validation.py
    - backend/lait/catalog/loader.py
    - backend/lait/application/queries/module_registry_describe.py
    - backend/lait/application/queries/exercise_registry_list_visible.py
    - backend/lait/adapters/http/routers/diagnostics.py
    - backend/lait/modules/exercise_gap_fill/manifest.json
    - backend/lait/modules/exercise_proof/manifest.json
  modified:
    - backend/lait/adapters/http/app.py

key-decisions:
  - "D-21 confirmed: visibility stays on exercise contributions; Phase 1 values are learner and maintainer; experimental is rejected"
  - "Universal manifests omit visibility; describe() allowlists public fields and marks every live row active"
  - "Runtime catalog checks use a Pydantic model mirrored by module-manifest.schema.json; no jsonschema package"
  - "Supported module api_version is 1; core.exercise-api 0.1.0 satisfies dependency specs"
  - "describe() orders by category then module_id; list_visible_for filters on contribution visibility only"

patterns-established:
  - "Pattern: bundled modules are discovered from lait/modules/*/manifest.json plus contribution.CONTRIBUTION"
  - "Pattern: create_app validates the catalog before opening SQLite and stores the registry on app.state"
  - "Pattern: lesson UI and the lessons router do not call module_registry.describe or GET /api/module-registry"

requirements-completed: [MODL-01, MODL-02, MODL-03]

coverage:
  - id: D1
    description: "Invalid, duplicate, empty, API-incompatible, and unresolved catalogs refuse startup; experimental visibility is rejected"
    requirement: MODL-01
    verification:
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_visibility_on_universal_manifest_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_duplicate_module_id_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_unresolved_dependency_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_empty_catalog_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_api_incompatible_manifest_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_missing_exercise_type_refuses_startup"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_experimental_visibility_is_rejected"
        status: pass
    human_judgment: false
  - id: D2
    description: "module_registry.describe returns Gap Fill and proof with the public field set and activation_status active"
    requirement: MODL-02
    verification:
      - kind: unit
        ref: "backend/tests/catalog/test_describe.py#test_describe_returns_public_active_rows"
        status: pass
      - kind: integration
        ref: "backend/tests/catalog/test_describe.py#test_http_module_registry_maps_describe"
        status: pass
    human_judgment: false
  - id: D3
    description: "list_visible_for(learner) returns Gap Fill and omits the maintainer proof contribution"
    requirement: MODL-03
    verification:
      - kind: unit
        ref: "backend/tests/catalog/test_list_visible_for.py#test_learner_list_includes_gap_fill_and_omits_proof"
        status: pass
      - kind: integration
        ref: "backend/tests/catalog/test_list_visible_for.py#test_http_exercise_registry_learner_returns_gap_fill_only"
        status: pass
    human_judgment: false
  - id: D4
    description: "Universal manifests have no visibility field; lesson feature code does not call describe"
    requirement: MODL-02
    verification:
      - kind: unit
        ref: "backend/tests/catalog/test_startup_validation.py#test_universal_manifests_and_schema_omit_visibility"
        status: pass
      - kind: unit
        ref: "backend/tests/catalog/test_list_visible_for.py#test_lesson_feature_does_not_call_module_registry_describe"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-10-01
status: complete
plan_head_before: 27036dd02720c72f1a32c9d1cc6de9fdc978f33e
plan_head_after: 28fc5c2cfe2d3c5c0f427c0f4cf228390b5c759b
---

# Phase 1 Plan 02: Static Catalog and Registry Queries Summary

**Startup-validated Gap Fill (`learner`) and proof (`maintainer`) catalog, with `module_registry.describe` and `exercise_registry.list_visible_for` behind DTO-only HTTP routes**

## Performance

- **Duration:** 25 min
- **Started:** 2026-10-01T05:03:21Z
- **Completed:** 2026-10-01T05:28:43Z
- **Tasks:** 3
- **Files modified:** 19

## Accomplishments

- An invalid, duplicate, empty, API-incompatible, or unresolved catalog raises before the process serves. `experimental` is not a live visibility value.
- `module_registry.describe()` returns Gap Fill and proof with public fields only. Every live row is `activation_status: active`.
- `exercise_registry.list_visible_for("learner")` returns Gap Fill and omits proof. `GET /api/exercise-registry?visibility=learner` and `GET /api/module-registry` map DTOs onto those queries.

## Task Commits

Each task was committed atomically:

1. **Task 1: Confirm D-21 one-way visibility placement** - decision only (`proceed-d21`), no commit
2. **Task 2: End-to-end catalog validate → describe → list_visible_for(learner)** - `7b33c3c` (test, RED) then `0f4b6f2` (feat, GREEN)
3. **Task 3: Expand invalid-catalog and uniqueness matrix** - `1497473` (test, RED) then `28fc5c2` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/catalog/validation.py` - schema, uniqueness, dependency, visibility, and empty-catalog checks
- `backend/lait/catalog/loader.py` - bundled `manifest.json` discovery; contribution import; entrypoints are not executed
- `backend/lait/catalog/manifests/module-manifest.schema.json` - universal manifest contract with no `visibility` property
- `backend/lait/modules/exercise_gap_fill/` - Gap Fill manifest and `visibility: learner`
- `backend/lait/modules/exercise_proof/` - proof manifest and `visibility: maintainer`
- `backend/lait/application/queries/module_registry_describe.py` - `module_registry.describe`
- `backend/lait/application/queries/exercise_registry_list_visible.py` - `exercise_registry.list_visible_for`
- `backend/lait/adapters/http/routers/diagnostics.py` - DTO mapping for the two GET routes
- `backend/lait/adapters/http/app.py` - validate the catalog once, then open SQLite

## Decisions Made

- Confirmed D-21: visibility stays on exercise contributions. Phase 1 accepts `learner` and `maintainer` only.
- `describe()` returns `module_id`, `module_version`, `category`, `capabilities`, `exercise_type`, `visibility`, and `activation_status`. It does not return names, publishers, dependencies, or source paths.
- Rows are ordered by category, then `module_id`. Learner filtering compares contribution visibility and does not branch on module id.
- Module API `1` is the only supported `api_version`. `core.exercise-api` `0.1.0` resolves `>=0.1.0`. A higher requirement is unresolved.
- The published JSON Schema and the Pydantic model agree. Runtime checks use Pydantic so this plan adds no schema package.

## TDD Gate Compliance

| Gate | Commit | Result |
|------|--------|--------|
| RED | `7b33c3c` `test(01-02): add failing test for catalog registry queries` | `RED_EVIDENCE_OK` / `target_test_failed` for `test_learner_list_includes_gap_fill_and_omits_proof` (exit 1, 10 failed) |
| GREEN | `0f4b6f2` `feat(01-02): implement catalog validation and registry queries` | tracer verify 12 passed |
| RED | `1497473` `test(01-02): add failing test for invalid catalog matrix` | `RED_EVIDENCE_OK` / `target_test_failed` for `test_missing_exercise_type_refuses_startup` (exit 1, 3 failed) |
| GREEN | `28fc5c2` `feat(01-02): reject empty, incompatible, and incomplete catalogs` | `uv run pytest backend/tests/catalog -q` 17 passed |
| REFACTOR | — | not needed |

Tracer feedback gate: `workflow.human_verify_mode` is `end-of-phase` and the tracer `<verify>` is automated-only. Re-ran the tracer command after GREEN (12 passed). Logged tracer verified end-to-end, then expanded into the invalid-catalog matrix.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] A bundled manifest without a contribution fails closed**
- **Found during:** Task 2 (catalog loader)
- **Issue:** Importing a missing `contribution` module would surface as `ModuleNotFoundError` from the composition root, which is not a catalog rejection the tests can classify.
- **Fix:** The loader raises `CatalogLoadError` when the bundled package has no `CONTRIBUTION`.
- **Files modified:** `backend/lait/catalog/loader.py`
- **Verification:** bundled Gap Fill and proof load; catalog tests pass
- **Committed in:** `0f4b6f2`

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** The loader still only reads build-time packages under `lait/modules`. Manifest entrypoints are not executed.

## Issues Encountered

- Starlette's `TestClient` warns that `httpx` is deprecated in favor of `httpx2`. The suite still passes. `httpx2` is not in STACK.md, so the tests stay on the installed TestClient.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for `01-03`. Gap Fill generate/evaluate bodies stay in `01-04`. Proof removal without Core edits stays in `01-09`. `MODL-03` is also declared by later plans, so the requirements checkbox stays open until those summaries exist.

## Self-Check: PASSED

- FOUND: `.planning/phases/01-mod-first-manual-learning-loop/01-02-SUMMARY.md`
- FOUND: `7b33c3c`
- FOUND: `0f4b6f2`
- FOUND: `1497473`
- FOUND: `28fc5c2`
- `main` remains `6d00e33`; commits are on `phase/01-execution`

## Known Stubs

None. Gap Fill and proof register contribution metadata only. Generate and evaluate bodies are deferred to plan `01-04`.

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
