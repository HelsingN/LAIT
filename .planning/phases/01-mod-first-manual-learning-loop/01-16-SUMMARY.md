---
phase: 01-mod-first-manual-learning-loop
plan: 16
subsystem: ui
tags: [practice, gap-fill, retry, corrected, score]

requires:
  - phase: 01-15
    provides: focus practice shell, session-scoped renderer key, and the current-pass score
provides:
  - same-session Try again, Show answer, and Continue
  - corrected only after an incorrect row for the same learning-unit id and mode
  - an automatic next round of still-uncorrected pairs
  - a first-try score over the opening pass size
affects: []

actuals:
  tokens: 0
  tasks: 5
  commits: 0

tech-stack:
  added: []
  patterns:
    - repeat copies share learning-unit id and mode; position is not the identity
    - pass_item_count is the opening pass size; session_item_count is the live row count

key-files:
  created: []
  modified:
    - backend/lait/application/commands/exercise_submit_attempt.py
    - backend/lait/application/commands/practice_advance.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/domain/practice_session.py
    - backend/lait/modules/exercise_gap_fill/feedback.py
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/stages/FeedbackStage.tsx
    - frontend/src/features/lesson/stageState.ts

key-decisions:
  - "A self-produced correct or corrected answer removes that pair. Show answer does not."
  - "The client names the learning unit. The handler uses the copy at the current cursor."
  - "The user approved this plan's Docker checkpoint on 2026-10-06. That approval does not close Phase 1."

patterns-established:
  - "Pattern: leaving the last item appends still-uncorrected opening pairs in the same session"

requirements-completed: []

coverage:
  - id: D1
    description: "A miss stays, a later match is corrected, and Continue on the last item starts the next uncorrected round or finishes."
    requirement: EXER-03
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_retry.py"
        status: pass
      - kind: manual_procedural
        ref: "C:/Users/97255/.codex/visualizations/2026/10/02/01a0fc72-fc87-7723-8dcf-da8bc00ec3f7/LAIT_01-16_AUTO_ROUNDS_BROWSER_CHECK.md"
        status: pass
    human_judgment: true
    rationale: "The user approved the Docker checkpoint on 2026-10-06 after the repeat-copy cursor fix. A real browser-process restart was not performed."
  - id: D2
    description: "The score is first-try correct over the opening pass size. Repeat rows do not change 6/8 into 6/10."
    requirement: EVAL-05
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_retry.py"
        status: pass
      - kind: automated_ui
        ref: "frontend/src/features/lesson/stages/FeedbackStage.test.tsx"
        status: pass
      - kind: manual_procedural
        ref: "C:/Users/97255/.codex/visualizations/2026/10/02/01a0fc72-fc87-7723-8dcf-da8bc00ec3f7/LAIT_01-16_AUTO_ROUNDS_BROWSER_CHECK.md"
        status: pass
    human_judgment: true
    rationale: "The user approved the Docker checkpoint on 2026-10-06. History still prints the expected phrase twice; that is deferred UX debt."

duration: 1d
completed: 2026-10-06
status: complete
---

# Phase 1 Plan 16: Same-Pass Retry and Automatic Rounds Summary

**A miss stays in the same session, a later match is corrected, and Continue keeps only the pairs that are still uncorrected.**

## Performance

- **Completed:** 2026-10-06
- **Tasks:** 4 implemented, 1 human-verify approved
- **Commits:** 0

## Accomplishments

- Try again clears the draft in the same session. Show answer reveals the phrase and writes no attempt.
- `corrected` is stored only when that learning-unit id and mode already has an `incorrect` row in the session.
- Leaving the last item appends still-uncorrected opening pairs. An empty queue finishes. Exit does not append.
- The listed denominator is the opening pass size. Disposition uses the live item count.
- A named target on a repeat copy advances that copy, not the original position.

## Task Commits

Uncommitted. The user has not asked for a commit.

## Decisions Made

- Do not offer Practice missed phrases. Do not open a second session for the round.
- Do not copy a reveal flag onto the new position.
- Phase 1 stays open. REQUIREMENTS.md stays unchanged.

## Deviations from Plan

- The first slice offered Practice missed phrases and kept corrected items. That path was removed before the checkpoint.
- `_resolve_item` took `matches[0]`, so a correct answer on a repeat copy set `advance` false and Continue reopened the same item. The current cursor copy now wins. Regression: `test_named_target_on_a_repeat_copy_advances_once`.

## User Setup Required

None.

## Next Phase Readiness

Plan 01-16 is complete. Phase 1 is not. A real browser-process restart was still a manual item at approval. History rows still repeat the expected phrase beside the unit jump. That is deferred UX debt, not a blocker.

## Self-Check: PASSED

- FOUND: backend/lait/application/commands/exercise_submit_attempt.py
- FOUND: backend/tests/application/test_practice_retry.py
- HUMAN: user approved the 01-16 checkpoint
- PHASE: not complete

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-06*
