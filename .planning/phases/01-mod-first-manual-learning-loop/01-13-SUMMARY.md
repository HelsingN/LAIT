---
phase: 01-mod-first-manual-learning-loop
plan: 13
subsystem: ui
tags: [practice-session, react, reopen, feedback]

requires:
  - phase: 01-12
    provides: open-session resume and practice.finish as the close
provides:
  - exercise.latest_completed restores a matching completed generation
  - attempt.list_for_lesson returns session id, mode, and disposition
  - last Continue closes an exhausted open session
  - current-pass summary stays on one session id
affects: [01-14-workspace-layout]

actuals:
  tokens: 0
  tasks: 3
  commits: 0

tech-stack:
  added: []
  patterns:
    - lesson reopen uses read queries, not exercise.generate
    - practice.finish remains the only close

key-files:
  created:
    - backend/lait/application/queries/exercise_latest_completed.py
    - backend/lait/application/queries/attempt_list_for_lesson.py
    - backend/tests/application/test_lesson_reopen_reads.py
    - backend/tests/adapters/persistence/test_lesson_reopen_reads.py
  modified:
    - backend/lait/application/ports.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/adapters/http/routers/exercises.py
    - backend/lait/adapters/http/routers/practice.py
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/stages/FeedbackStage.tsx
    - frontend/src/api/generated/

key-decisions:
  - "A completed generation is restorable only when its accepted ids match the current accepted set"
  - "The pass summary shows one session id; other sessions stay under Earlier passes"
  - "An exhausted open session is closed with the existing practice.finish"
  - "Finish 404 clears the stored id; finish 500 keeps it and does not show a completed summary"

patterns-established:
  - "Pattern: GET exercises/latest and GET attempts hydrate the workspace"

requirements-completed: [EXER-02, EXER-07]

coverage:
  - id: D1
    description: "Reload restores a matching generation and saved attempts without exercise.generate. A mismatched accepted set stays locked."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "backend/tests/application/test_lesson_reopen_reads.py"
        status: pass
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
    human_judgment: false
  - id: D2
    description: "The last Continue closes the exhausted session and the summary contains only that session id. An early Exit is exited."
    requirement: EXER-07
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/stages/FeedbackStage.test.tsx"
        status: pass
    human_judgment: false
  - id: D3
    description: "Docker reopen, full pass, and early exit on the Compose app."
    requirement: EXER-02
    verification:
      - kind: manual_procedural
        ref: "docs/audits/PHASE1_UX_AUDIT_2026-10-02.md#повторная-ручная-проверка-среза-01-13"
        status: pass
    human_judgment: true
    rationale: "The user approved only this plan's six-scenario checkpoint. That approval does not close Phase 1."

duration: 90min
completed: 2026-10-02
status: complete
---

# Phase 1 Plan 13: Reopen And Pass Completion Summary

**Reload reads the matching generation and saved attempts, and the last Continue closes that session instead of leaving an empty Focus screen.**

## Performance

- **Completed:** 2026-10-02
- **Tasks:** 2 implemented, 1 human-verify approved
- **Commits:** 0. The user forbade commit and push. The work remains in the working tree on `phase/01-execution`.

## Accomplishments

- `exercise.latest_completed` returns `restorable: true` only when the latest completed generation's accepted ids match the current accepted set.
- `attempt.list_for_lesson` returns each attempt with `session_id`, `mode`, and `session_disposition`.
- Workspace load does not call `exercise.generate`.
- The last Continue, and a stored open session with no current item, call `practice.finish`. A 404 clears the stored id. A 500 keeps it and does not show a completed summary.
- The current-pass summary is one `session_id`. Other sessions render under Earlier passes.

## Task Commits

None. Implementation is uncommitted by user instruction.

## Decisions Made

- No `practice.complete` command. The existing `practice.finish` closes an exhausted open session.
- Phase 1 stays open. This summary does not mark the phase checkbox.

## Deviations from Plan

- `pyproject.toml` sets pytest `importlib` import mode so the two `test_lesson_reopen_reads.py` modules collect together.
- `test_openapi_contract.py` expects the two new operation ids.

## User Setup Required

None.

## Next Phase Readiness

Plan 01-13 is complete. Phase 1 is not. Slice 2 is plan 01-14 and is not started. Feedback still reads as a technical log; that learning-summary redesign stays in a later slice and is not a blocker of this plan.

## Self-Check: PASSED

- FOUND: backend/lait/application/queries/exercise_latest_completed.py
- FOUND: backend/lait/application/queries/attempt_list_for_lesson.py
- FOUND: frontend/src/features/lesson/stages/FeedbackStage.tsx
- HUMAN: user approved the 01-13 checkpoint only
- PHASE: not complete

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-02*
