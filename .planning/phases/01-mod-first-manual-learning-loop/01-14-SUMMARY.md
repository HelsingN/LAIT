---
phase: 01-mod-first-manual-learning-loop
plan: 14
subsystem: ui
tags: [layout, react, workspace, feedback-cover]

requires:
  - phase: 01-13
    provides: restored generation, attempt history, and the current-pass summary
provides:
  - wide preparation is side by side from 960px and stacked below
  - panes scroll inside a height floor instead of growing the page
  - a short window covers preparation with Feedback and restores it on close
  - Exercises header and ready stay visible while Feedback history scrolls
affects: []

actuals:
  tokens: 0
  tasks: 5
  commits: 0

tech-stack:
  added: []
  patterns:
    - preparation slot is flex 1 1 0 with track floors of 188px wide and 88px plus 232px narrow
    - open Feedback covers that slot only when the viewport cannot also hold a 160px body
    - Feedback history is the only flex child that shrinks inside the action column

key-files:
  created: []
  modified:
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/LessonWorkspacePage.module.css
    - frontend/src/features/lesson/LessonWorkspacePage.test.tsx
    - frontend/src/features/lesson/stages/LearningUnitsStage.tsx
    - frontend/src/features/lesson/stages/LearningUnitsStage.module.css
    - frontend/src/features/lesson/stages/SourceStage.module.css
    - frontend/src/features/lesson/stages/GenerateExercisesStage.module.css

key-decisions:
  - "Side by side starts at min-width 960px. A fractional width between 959 and 960 stays stacked."
  - "Closed Feedback at 959×700 keeps Add, two unit rows, and Start inside the window."
  - "A 26px Feedback body is not a readable panel. Below the height test, Feedback covers the preparation slot."
  - "Preparation stays mounted while covered, so the text range and scroll positions remain."
  - "Feedback history scrolls in its own panel. The Exercises header and ready line do not shrink with it."

patterns-established:
  - "Pattern: short-window Feedback uses the preparation slot; a taller window keeps both"

requirements-completed: []

coverage:
  - id: D1
    description: "From 960px Source and units sit side by side. Below that they stack. Add stays outside the unit scroller. The selected unit deletes with a compact × named Remove {phrase}."
    requirement: ANLY-08
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LearningUnitsStage.test.tsx"
        status: pass
    human_judgment: false
  - id: D2
    description: "A restorable generation says Exercises are ready. Generate Exercises is not the next step for an unchanged accepted set. Stage headers expose aria-expanded."
    requirement: EXER-01
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
    human_judgment: false
  - id: D3
    description: "On a short window, open Feedback covers preparation and closing it restores Source, units, selection, and scroll. On 1280×800 the Exercises header and ready line stay visible beside a scrolling Feedback history."
    requirement: LESS-01
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
      - kind: manual_procedural
        ref: "docs/audits/PHASE1_UX_AUDIT_2026-10-02.md#подтверждение-исправления-ux-20--2026-10-05-checkpoint-01-14-approved"
        status: pass
    human_judgment: true
    rationale: "The user approved only this plan's three-scenario checkpoint on 2026-10-05. UX-20 did not reproduce. That approval does not close Phase 1."

duration: 1d
completed: 2026-10-05
status: complete
---

# Phase 1 Plan 14: Workspace Layout Summary

**Preparation and the main actions fit the window, and a short window gives Feedback the preparation slot instead of a slit.**

## Performance

- **Completed:** 2026-10-05
- **Tasks:** 4 implemented, 1 human-verify approved
- **Commits:** 0. The user forbade commit and push. The work remains in the working tree on `phase/01-execution`.

## Accomplishments

- From 960px Source and units share one row. Below 960px they stack. Add sits above the unit list.
- The selected row shows `×`. Its accessible name is `Remove {phrase}`.
- Closed Feedback at 959×700 keeps Add, two full unit rows, and Start visible.
- When the viewport cannot also hold a 160px Feedback body, the open panel covers the preparation slot. Closing it restores the same panes.
- At 1280×800 an open history scrolls inside Feedback. The Exercises header and "Exercises are ready." stay visible.

## Task Commits

None. Implementation is uncommitted by user instruction.

## Decisions Made

- Do not leave Feedback a 26px body. Cover the preparation slot on a short window.
- Do not let Feedback history shrink the Exercises section.
- Phase 1 stays open. This summary does not mark the phase checkbox.
- LESS-01, ANLY-08, and EXER-01 stay Gaps Found in `REQUIREMENTS.md`. This plan does not close them.

## Deviations from Plan

- UX-18 and UX-19 were layout bugs of the first 01-14 build. The height floors and the short-window cover replaced `minmax(min-content, 1fr)` and the 32dvh Feedback cap.
- UX-20 clipped Exercises to about 9px when Feedback history was open at 1280×800. The history panel is now the only shrinking region in the action column.
- On 1280×520 the exercise-type line can shrink to about 10px. The Exercises header, ready line, Start, and Feedback header stay whole. The user accepted that checkpoint.

## User Setup Required

None.

## Next Phase Readiness

Plan 01-14 is complete. Phase 1 is not. Practice chip order, typed-field chrome, and the Feedback learning summary stay in later slices. Feedback still reads as a technical log.

## Self-Check: PASSED

- FOUND: frontend/src/features/lesson/LessonWorkspacePage.module.css
- FOUND: frontend/src/features/lesson/LessonWorkspacePage.tsx
- HUMAN: user approved the 01-14 checkpoint only
- PHASE: not complete

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-05*
