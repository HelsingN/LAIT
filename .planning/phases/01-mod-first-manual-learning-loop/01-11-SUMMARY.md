---
phase: 01-mod-first-manual-learning-loop
plan: 11
subsystem: api
tags: [practice-session, fastapi, attempt]

requires:
  - phase: 01-05
    provides: practice.start, an open session as the freeze flag, and restrict-linked Attempt rows
provides:
  - practice.finish closes the session and unfreezes the accepted unit set
  - practice.start_over abandons in-progress state, keeps Attempts, then calls practice.start
  - POST finish and start-over map DTOs only
affects: [01-07]

actuals:
  tokens: 5432
  tasks: 1
  commits: 2

tech-stack:
  added: []
  patterns:
    - closed and abandoned are the two non-open session statuses
    - start-over orchestration lives in practice.start_over and then calls practice.start
    - practice HTTP maps a DTO onto one command

key-files:
  created:
    - backend/lait/application/commands/practice_finish.py
    - backend/lait/application/commands/practice_start_over.py
  modified:
    - backend/lait/adapters/http/routers/practice.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/application/queries/practice_get.py
    - backend/lait/domain/practice_session.py

key-decisions:
  - "practice.finish sets status closed and returns no current item, so the open-session freeze lifts"
  - "practice.start_over sets status abandoned, keeps Attempt rows, then calls practice.start on the same lesson"
  - "If practice.start refuses after that abandon, the session is restored to open so the unit set stays frozen"
  - "POST finish and POST start-over only map DTOs; the router does not abandon state and does not call practice.start"

patterns-established:
  - "Pattern: a non-open session does not serve a current item"
  - "Pattern: Start Over is practice.start_over, not a parameter of practice.finish"

requirements-completed: [EXER-07]

coverage:
  - id: D1
    description: "practice.finish closes the session, hides the current item, keeps Attempts, and unfreezes units"
    requirement: EXER-07
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_finish_and_start_over.py#test_finish_closes_session_and_unfreezes_units"
        status: pass
    human_judgment: false
  - id: D2
    description: "practice.start_over keeps Attempt rows, opens a new session via practice.start, and leaves units frozen"
    requirement: EXER-07
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_finish_and_start_over.py#test_start_over_keeps_attempts_and_leaves_units_frozen"
        status: pass
    human_judgment: false
  - id: D3
    description: "POST finish and POST start-over return 200 and the handler bodies only map DTOs onto practice.finish and practice.start_over"
    requirement: EXER-07
    verification:
      - kind: integration
        ref: "backend/tests/application/test_practice_finish_and_start_over.py#test_http_finish_and_start_over_only_map_dtos"
        status: pass
    human_judgment: false

duration: 1h 45m
completed: 2026-10-01
status: complete
plan_head_before: 3761d1f068ca9c742a003c0bc252b4f4cd041e22
plan_head_after: cd869f343d7f04eeb70b7af514a9fbaac43f099b
---

# Phase 1 Plan 11: Finish and Start Over Summary

**practice.finish closes the session and unfreezes units; practice.start_over keeps Attempts and calls practice.start so the same accepted set stays frozen**

## Performance

- **Duration:** 1h 45m
- **Started:** 2026-10-01T21:35:59Z
- **Completed:** 2026-10-01T23:21:11Z
- **Tasks:** 1
- **Files modified:** 8

## Accomplishments

- `practice.finish` sets the session to `closed`, returns `open=false` with no current item, leaves Attempt rows in place, and unfreezes the unit set because no session stays open.
- `practice.start_over` sets the session to `abandoned`, does not delete Attempt rows, then calls the existing `practice.start`. The new session is open, so add, remove, and accept stay frozen.
- `POST /api/practice-sessions/{session_id}/finish` and `POST /api/practice-sessions/{session_id}/start-over` map the path id onto those commands. The handlers do not abandon state and do not call `practice.start`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Expand finish vs Start Over** - `1dd70db` (test, RED) then `cd869f3` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/application/commands/practice_finish.py` - close the session and return a workspace view
- `backend/lait/application/commands/practice_start_over.py` - abandon non-attempt state, keep Attempts, call `practice.start`
- `backend/lait/adapters/http/routers/practice.py` - DTO-only finish and start-over routes
- `backend/lait/adapters/persistence/repositories.py` - `set_practice_session_status`
- `backend/lait/domain/practice_session.py` - `closed` and `abandoned` statuses
- `backend/lait/application/queries/practice_get.py` - a non-open session has no current item
- `backend/tests/application/test_practice_finish_and_start_over.py` - finish, start-over, and HTTP mapping
- `backend/tests/application/test_submit_attempt.py` - drop the 01-05 assertion that finish routes are absent

## Decisions Made

- Finish and Start Over are different statuses: `closed` versus `abandoned`. `practice.finish` is not a parameterised alias for Start Over.
- Start Over does not edit `practice_start.py`. It marks the current session abandoned, then calls `practice.start`, which inserts a new open session on the same generation.
- Attempt rows are never deleted by either command. The session foreign key stays `ON DELETE RESTRICT`; only the status column changes.
- If `practice.start` raises after the abandon write, `practice.start_over` puts that session back to `open` before re-raising, so a refused restart does not unfreeze the set.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Persist a session status change**
- **Found during:** Task 1 (Expand finish vs Start Over)
- **Issue:** `save_practice_session` only inserts. Closing or abandoning a session had no write path, so finish could not unfreeze and start-over could not call `practice.start` while an open session still existed.
- **Fix:** `set_practice_session_status` updates the status column and does not delete Attempt rows.
- **Files modified:** `backend/lait/adapters/persistence/repositories.py`, `backend/lait/domain/practice_session.py`
- **Verification:** `test_finish_closes_session_and_unfreezes_units` and `test_start_over_keeps_attempts_and_leaves_units_frozen` pass
- **Committed in:** `cd869f3` (Task 1 GREEN)

**2. [Rule 2 - Missing Critical] A non-open session does not serve a current item**
- **Found during:** Task 1 (Expand finish vs Start Over)
- **Issue:** `view_for` built `current` from the cursor even after the session was closed, so practice.get would still present the exercise.
- **Fix:** `view_for` builds `current` only when the session status is open.
- **Files modified:** `backend/lait/application/queries/practice_get.py`
- **Verification:** finish returns `current is None` and `viewed.current is None`; open-session practice tests still pass
- **Committed in:** `cd869f3` (Task 1 GREEN)

**3. [Rule 2 - Missing Critical] Restore the open session if practice.start refuses**
- **Found during:** Task 1 (Expand finish vs Start Over)
- **Issue:** Abandon commits before `practice.start`. A later refusal would leave no open session and unfreeze the unit set.
- **Fix:** On any exception from `practice.start`, set the abandoned session back to `open` and re-raise.
- **Files modified:** `backend/lait/application/commands/practice_start_over.py`
- **Verification:** the happy-path start-over test stays frozen; `practice_start.py` is unchanged
- **Committed in:** `cd869f3` (Task 1 GREEN)

**4. [Rule 1 - Bug] 01-05 HTTP test forbade the routes this plan adds**
- **Found during:** Task 1 (Expand finish vs Start Over)
- **Issue:** `test_http_maps_generate_start_get_and_submit_only` asserted `practice.finish` and `practice.start_over` were absent from the router and OpenAPI.
- **Fix:** Keep the assertions that generate, start, get, and submit still map, and that the router does not import the persistence package. The new test owns finish and start-over.
- **Files modified:** `backend/tests/application/test_submit_attempt.py`
- **Verification:** `test_http_maps_generate_start_get_and_submit_only` passes with the new routes present
- **Committed in:** `cd869f3` (Task 1 GREEN)

---

**Total deviations:** 4 auto-fixed (3 missing critical, 1 bug)
**Impact on plan:** The status write is what makes finish and start-over different outcomes. No new package, no MCP, and no edit to `practice_start.py`.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 finish vs Start Over | `1dd70db` `RED_EVIDENCE_OK` / `target_test_failed` for `test_finish_closes_session_and_unfreezes_units` (exit 1, 3 failed) | `cd869f3` | — | Pass |

## Authentication Gates

None.

## Issues Encountered

None in this plan's tests. `uv run pytest backend/tests -q` also reports two failures that read frontend sources this plan did not change: `test_lesson_list_ui_locks_copy_and_self_hosted_fonts` and `test_lesson_feature_does_not_call_module_registry_describe`. Left untouched.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for plan 01-07. Exit Practice can call `practice.finish`. Start Over can call `practice.start_over` and must not assemble abandon-plus-start in the client or the router.
- EXER-07 is also declared by plan 01-07, so the requirement checkbox stays open until that plan's summary exists.
- `backend/lait/application/commands/practice_start.py` was not modified.

## Self-Check: PASSED

- FOUND: `backend/lait/application/commands/practice_finish.py`
- FOUND: `backend/lait/application/commands/practice_start_over.py`
- FOUND: `backend/lait/adapters/http/routers/practice.py`
- FOUND: `1dd70db`
- FOUND: `cd869f3`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
