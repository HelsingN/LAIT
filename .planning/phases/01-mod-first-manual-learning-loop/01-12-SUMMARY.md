---
phase: 01-mod-first-manual-learning-loop
plan: 12
subsystem: api
tags: [practice-session, sqlite, alembic, react, localStorage]

requires:
  - phase: 01-05
    provides: practice.start freezes the accepted set and raises StaleGenerationError for a stale snapshot
  - phase: 01-07
    provides: Focus Practice chrome and Exit Practice calling practice.finish
  - phase: 01-11
    provides: practice.start_over abandons then calls practice.start
provides:
  - practice.start returns the open session when its generation snapshot matches
  - partial unique index uq_practice_sessions_one_open_per_lesson
  - per-lesson localStorage resume into Focus Practice
  - Start Practice disabled until the start request settles
affects: [01-verification]

actuals:
  tokens: 9236
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - insert_open_practice_session selects and inserts in one transaction
    - isPracticeOpen(pendingStoredSession, sessionOpen) ignores focused
    - Start Practice pending is cleared in finally

key-files:
  created:
    - backend/alembic/versions/20261002_0004_one_open_practice_session.py
    - frontend/src/features/lesson/stages/PracticeStage.test.tsx
  modified:
    - backend/lait/application/commands/practice_start.py
    - backend/lait/adapters/persistence/repositories.py
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/stageState.ts

key-decisions:
  - "practice.start returns the open session only when that session's generation accepted_unit_ids match the current accepted set"
  - "A mismatched open snapshot raises StaleGenerationError and does not close the row"
  - "isPracticeOpen is true while a stored session load is pending, otherwise it follows session.open"
  - "A ref blocks a second Start Practice click before the disabled button paints"

patterns-established:
  - "Pattern: lait.practice-session.{lessonId} is the open session id for that lesson"
  - "Pattern: one open practice row per lesson is enforced by a partial unique index"

requirements-completed: [EXER-02]

coverage:
  - id: D1
    description: "A second practice.start returns the same session when the accepted-set snapshot matches, including after generate again."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_second_start_returns_the_same_open_session"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_generate_again_keeps_the_open_session_for_the_next_start"
        status: pass
    human_judgment: false
  - id: D2
    description: "A second open row for one lesson cannot commit, and a unique violation returns the winning session id."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_second_open_row_for_one_lesson_is_rejected"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_practice_start.py#test_unique_violation_returns_the_winning_open_session"
        status: pass
    human_judgment: false
  - id: D3
    description: "A stored lait.practice-session id shows the frozen hint while practice.get is pending, then resumes Focus Practice when the session is open."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#resumes a stored open session into Focus Practice after the frozen hint"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#isPracticeOpen locks while a stored session is pending and then follows session.open"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#clears a stored session that is not open and leaves the workspace unlocked"
        status: pass
    human_judgment: false
  - id: D4
    description: "Start Practice stays disabled until the first start request settles, including when that request fails."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/stages/PracticeStage.test.tsx#disables Start Practice while the start request is pending"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#disables Start Practice until the first start request settles"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#enables Start Practice again after the start request rejects"
        status: pass
    human_judgment: false

duration: 35min
completed: 2026-10-02
status: complete
plan_head_before: 38c6c3203e599272bcc4d9e8416c84f65bcce1f1
plan_head_after: 2f5f082838e842b8ee13bb3b24e3b694868c9432
---

# Phase 1 Plan 12: Open Session Resume Summary

**practice.start returns the same-generation open session, one open row is unique per lesson, and a refresh restores Focus Practice from lait.practice-session.{lessonId}**

## Performance

- **Duration:** 35 min
- **Started:** 2026-10-02T02:00:00Z
- **Completed:** 2026-10-02T02:35:28Z
- **Tasks:** 2
- **Files modified:** 11

## Accomplishments

- `practice.start` returns the existing open session when that session's generation `accepted_unit_ids` match the current accepted set. A mismatch raises `StaleGenerationError`, leaves the row open, and leaves units frozen.
- Revision `20261002_0004` is the Alembic head. `uq_practice_sessions_one_open_per_lesson` rejects a second open row. `insert_open_practice_session` checks and inserts in one transaction and re-reads the winner after `IntegrityError`.
- The workspace stores the open session id at `lait.practice-session.${lessonId}`. On load it calls `practice.get`, shows the Learning Units frozen hint while that call is pending, then opens Focus Practice when the view is open. Exit Practice remains the `practice.finish` call.
- Start Practice stays disabled until the first start request settles. A second click during that request does not call `practice.start` again.

## Task Commits

Each task was committed atomically:

1. **Task 1: Resume the same-generation open session end to end** - `c72f877` (test, RED) then `756b0cc` (feat, GREEN)
2. **Task 2: Block a second open row and a double Start Practice** - `cf0f0bb` (test, RED) then `2f5f082` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/application/commands/practice_start.py` - return the matching open session instead of always raising
- `backend/lait/application/ports.py` - `insert_open_practice_session` on the learning-unit port
- `backend/lait/adapters/persistence/repositories.py` - one-transaction insert and winner re-read
- `backend/lait/adapters/persistence/models.py` - partial unique index on open rows
- `backend/alembic/versions/20261002_0004_one_open_practice_session.py` - create and drop only that index
- `backend/tests/application/test_practice_start.py` - same-generation return, stale open snapshot, unique violation
- `frontend/src/features/lesson/stageState.ts` - per-lesson session id and `isPracticeOpen`
- `frontend/src/features/lesson/LessonWorkspacePage.tsx` - restore, persist, and in-flight start lock
- `frontend/src/features/lesson/stages/PracticeStage.tsx` - disable Start Practice while `pending`
- `frontend/src/features/lesson/LessonWorkspacePage.test.tsx` - resume and in-flight start
- `frontend/src/features/lesson/stages/PracticeStage.test.tsx` - pending and disabled button

## Decisions Made

- The open session is returned only when `tuple(sorted(generation.accepted_unit_ids))` for that session's `generation_id` equals the current accepted ids. A newer completed generation with the same ids does not close the open row.
- When the latest generation does not match and an open row exists, `practice.start` compares that row's snapshot and does not insert. `get_open_practice_session` is the read used for that branch.
- `isPracticeOpen(pendingStoredSession, sessionOpen)` is true while the stored id's `practice.get` has not settled, otherwise it returns `sessionOpen`. `focused` is not a parameter. The workspace passes that value into `LearningUnitsStage`.
- `handleStart` sets a ref before `await startPractice` and clears it in `finally`, so a second click cannot send another start even before the disabled button paints.

## Deviations from Plan

None - plan executed exactly as written.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 same-generation resume | `c72f877` `RED_EVIDENCE_OK` / `target_test_failed` for `test_second_start_returns_the_same_open_session` (exit 1, `StaleGenerationError`) | `756b0cc` | — | Pass |
| 2 one open row and in-flight start | `cf0f0bb` `RED_EVIDENCE_OK` / `target_test_failed` for `PracticeStage.test.tsx` pending button (exit 1, button stayed enabled) | `2f5f082` | — | Pass |

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

EXER-02 is unblocked for this gap: refresh restores the open Gap Fill session, a second start returns that session when the snapshot matches, a second open row cannot commit, and Start Practice cannot fire twice before the first request settles. `practice.finish` and `practice.start_over` were not edited. Phase 01 is ready for verification.

## Self-Check: PASSED

- FOUND: backend/alembic/versions/20261002_0004_one_open_practice_session.py
- FOUND: frontend/src/features/lesson/stages/PracticeStage.test.tsx
- FOUND: c72f877
- FOUND: 756b0cc
- FOUND: cf0f0bb
- FOUND: 2f5f082

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-02*
