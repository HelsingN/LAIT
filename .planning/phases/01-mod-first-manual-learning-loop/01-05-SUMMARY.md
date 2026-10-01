---
phase: 01-mod-first-manual-learning-loop
plan: 05
subsystem: api
tags: [practice-session, exercise-generate, attempt, sqlite, fastapi]

requires:
  - phase: 01-03
    provides: accepted learning units and reject_if_unit_set_frozen
  - phase: 01-04
    provides: learner-visible generate and evaluate callables
provides:
  - exercise.generate persists completed or failed with the accepted-unit id set
  - practice.start freezes that set and serves one current item
  - N>1 sessions walk drag then typed; one unit is typed only
  - exercise.submit_attempt stores a restrict-linked Attempt and leaves the session open
affects: [01-06, 01-07, 01-11]

actuals:
  tokens: 21042
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - terminal generation status committed with its definitions
    - open PracticeSession is the freeze flag
    - catalog package name loads generate and evaluate
    - Attempt copies unit id, code-point span, and unit text at submit

key-files:
  created:
    - backend/lait/application/commands/exercise_generate.py
    - backend/lait/application/commands/practice_start.py
    - backend/lait/application/commands/exercise_submit_attempt.py
    - backend/lait/application/queries/practice_get.py
    - backend/lait/domain/practice_session.py
    - backend/lait/adapters/http/routers/exercises.py
    - backend/lait/adapters/http/routers/practice.py
    - backend/alembic/versions/20261001_0003_create_practice_sessions.py
  modified:
    - backend/lait/adapters/persistence/models.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/catalog/loader.py
    - backend/lait/catalog/validation.py
    - backend/lait/adapters/http/routers/__init__.py

key-decisions:
  - "exercise.generate commits only completed or failed, together with the accepted-unit id set"
  - "practice.start rejects when that set differs from the current accepted units; a draft-only add does not"
  - "An open PracticeSession is what has_open_practice_session reports; the unit commands are unchanged"
  - "N>1 is drag across the span order, then typed; one accepted unit is typed only"
  - "Attempt.learning_unit_id is ON DELETE RESTRICT and stores the span and unit text captured at submit"

patterns-established:
  - "Pattern: learner-visible modules are selected with list_visible_for, then loaded by catalog package name"
  - "Pattern: practice HTTP maps start, get, and submit only; finish and start-over stay on the later plan"
  - "Pattern: a second accepted submit of the same reached item inserts another Attempt"

requirements-completed: [EXER-01, EXER-02, EXER-07]

coverage:
  - id: D1
    description: "exercise.generate stores completed with one definition per accepted unit, and failed with zero definitions when none are accepted"
    requirement: EXER-01
    verification:
      - kind: unit
        ref: "backend/tests/application/test_exercise_generate.py#test_generate_with_accepted_units_stores_completed_and_matching_count"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_exercise_generate.py#test_generate_with_zero_accepted_stores_failed_and_zero_definitions"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_exercise_generate.py#test_generate_skips_drafts_and_persists_only_terminal_status"
        status: pass
    human_judgment: false
  - id: D2
    description: "practice.start freezes add, remove, and accept while the session is open, and rejects a stale accepted-unit set"
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_start_freezes_add_remove_and_accept"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_start_rejects_stale_generation_after_accept_or_remove"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_draft_only_add_does_not_invalidate_generation"
        status: pass
    human_judgment: false
  - id: D3
    description: "practice.get returns one current item; two units are drag then typed in span order, and one unit is typed only"
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_practice_get_returns_one_current_typed_item_for_one_unit"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_two_unit_lesson_yields_drag_then_typed_in_span_order"
        status: pass
    human_judgment: false
  - id: D4
    description: "Submit stores feedback and an Attempt, advances the cursor, keeps the session open, and accepts a second submit of the same item"
    requirement: EXER-07
    verification:
      - kind: unit
        ref: "backend/tests/application/test_submit_attempt.py#test_submit_stores_attempt_feedback_and_advances_while_session_stays_open"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_submit_attempt.py#test_same_item_accepted_twice_creates_two_attempts"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_submit_attempt.py#test_attempt_unit_fk_is_on_delete_restrict_and_copies_span_and_text"
        status: pass
    human_judgment: false
  - id: D5
    description: "HTTP maps generate, start, get, and submit, and does not add finish or start-over routes"
    requirement: EXER-07
    verification:
      - kind: integration
        ref: "backend/tests/application/test_submit_attempt.py#test_http_maps_generate_start_get_and_submit_only"
        status: pass
    human_judgment: false

duration: 2h 38m
completed: 2026-10-01
status: complete
plan_head_before: 86bd831e191b44b3be8d676c661173c74973effa
plan_head_after: 19cce38d9ec37f38a02afec514eaf229366a302b
---

# Phase 1 Plan 05: Generate, Practice Start, and Submit Summary

**exercise.generate stores a terminal accepted-unit snapshot, practice.start freezes that set into one current item, and submit records a restrict-linked Attempt while the session stays open**

## Performance

- **Duration:** 2h 38m
- **Started:** 2026-10-01T07:44:57Z
- **Completed:** 2026-10-01T10:22:48Z
- **Tasks:** 2
- **Files modified:** 16

## Accomplishments

- `exercise.generate` reads accepted units through `list_visible_for("learner")`, commits `completed` or `failed` in one write, and stores the accepted-unit id set. An empty accepted pool is `failed` with zero definitions.
- `practice.start` rejects when that set differs from the current accepted units. Adding a draft does not invalidate it. An open session makes `has_open_practice_session` true, so the existing add, remove, and accept commands freeze.
- Two accepted units walk drag, drag, then typed, typed, ordered by span start then unit id. One accepted unit is typed only. `practice.get` returns the current item.
- `exercise.submit_attempt` evaluates on the server, stores the unit id, code-point span, and unit text, and leaves the session open. A second accepted submit of the same item inserts another Attempt. The unit foreign key is `ON DELETE RESTRICT`.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end generate → start → submit → next item** - `27f7acd` (test, RED) then `26ead58` (feat, GREEN)
2. **Task 2: Expand N>1 drag-then-typed pass sequencing** - `e9f6bdc` (test, RED) then `19cce38` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/application/commands/exercise_generate.py` - terminal generation from learner-visible modules
- `backend/lait/application/commands/practice_start.py` - freeze, stale-set check, pass list
- `backend/lait/application/commands/exercise_submit_attempt.py` - Attempt plus feedback
- `backend/lait/application/queries/practice_get.py` - one current item
- `backend/lait/domain/practice_session.py` - generation, session, attempt, stale error
- `backend/lait/adapters/persistence/models.py` - generation, definition, session, pass item, attempt tables
- `backend/lait/adapters/persistence/repositories.py` - open-session lookup and the practice writes
- `backend/alembic/versions/20261001_0003_create_practice_sessions.py` - `ON DELETE RESTRICT` revision
- `backend/lait/adapters/http/routers/exercises.py` - `exercise.generate` DTO mapping
- `backend/lait/adapters/http/routers/practice.py` - start, get, submit only
- `backend/lait/catalog/loader.py` - load generate and evaluate by package name
- `backend/lait/catalog/validation.py` - package name on the catalog record
- `backend/tests/application/test_exercise_generate.py` - terminal status and accepted-set snapshot
- `backend/tests/application/test_practice_start.py` - freeze, stale set, pass order
- `backend/tests/application/test_submit_attempt.py` - Attempt durability and HTTP mapping

## Decisions Made

- Generation status is only `completed` or `failed`, committed with its definitions and the accepted-unit id set.
- `practice.start` compares that set to the live accepted ids. Accept, or remove of an accepted unit, makes the generation stale. A draft add does not.
- Freeze stays inside `reject_if_unit_set_frozen`. This plan only makes `has_open_practice_session` true for an open session. The three unit command modules were not edited.
- Pass order is span start, then learning unit id. More than one unit is a drag pass then a typed pass. One unit skips drag.
- Submit is not idempotent. Repeating a reached item inserts another Attempt. The cursor advances only when the submitted item is the current one.
- A second `practice.start` while a session is already open is rejected, so start-over can close the old session before calling start.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Parent row is flushed before child inserts**
- **Found during:** Task 1 (End-to-end generate → start → submit → next item)
- **Issue:** SQLite checked the definition foreign key before the generation row in the same commit was visible, so a successful generate raised `IntegrityError`.
- **Fix:** Flush the generation row, then insert definitions. The same order is used for a session and its pass items.
- **Files modified:** `backend/lait/adapters/persistence/repositories.py`
- **Verification:** `test_generate_with_accepted_units_stores_completed_and_matching_count` passes
- **Committed in:** `26ead58` (Task 1 GREEN)

**2. [Rule 2 - Missing Critical] Catalog records carry the bundled package name**
- **Found during:** Task 1 (End-to-end generate → start → submit → next item)
- **Issue:** `list_visible_for` returns module ids, and core must not hard-code a module id or package to call `generate` / `evaluate`.
- **Fix:** The loader stores the manifest directory name on `ModuleRecord.package`. Application imports `lait.modules.<package>.generate` and `.evaluate` from that name.
- **Files modified:** `backend/lait/catalog/validation.py`, `backend/lait/catalog/loader.py`
- **Verification:** `test_core_does_not_special_case_exercise_module_ids` passes, and generate still selects only the learner-visible module
- **Committed in:** `26ead58` (Task 1 GREEN)

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 missing critical)
**Impact on plan:** Both keep generation and grading on the public module contract. No new package, no MCP, and no edits to the unit command modules.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 generate/start/submit | `27f7acd` `RED_EVIDENCE_OK` / `target_test_failed` for `test_generate_with_accepted_units_stores_completed_and_matching_count` (exit 1, 12 failed) | `26ead58` | — | Pass |
| 2 drag-then-typed | `e9f6bdc` `RED_EVIDENCE_OK` / `target_test_failed` for `test_two_unit_lesson_yields_drag_then_typed_in_span_order` (exit 1, assertion `['typed', 'typed']`) | `19cce38` | — | Pass |

Tracer task 1 was re-run after GREEN (`12 passed`) before the drag-then-typed test was added.

## Authentication Gates

None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for the lesson UI and for plan 01-11. `practice.finish` and `practice.start_over` are not on the router. Start-over can abandon the open session and then call `practice.start`.
- EXER-01 is also declared by plan 01-06, EXER-02 by plan 01-07, and EXER-07 by plans 01-07 and 01-11, so those requirement checkboxes stay open until those plans finish.
- Full backend suite: 79 passed.

## Self-Check: PASSED

- FOUND: `backend/lait/application/commands/exercise_generate.py`
- FOUND: `backend/lait/application/commands/practice_start.py`
- FOUND: `backend/lait/application/commands/exercise_submit_attempt.py`
- FOUND: `backend/lait/application/queries/practice_get.py`
- FOUND: `backend/lait/domain/practice_session.py`
- FOUND: `backend/lait/adapters/http/routers/practice.py`
- FOUND: `backend/alembic/versions/20261001_0003_create_practice_sessions.py`
- FOUND: `27f7acd`
- FOUND: `26ead58`
- FOUND: `e9f6bdc`
- FOUND: `19cce38`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
