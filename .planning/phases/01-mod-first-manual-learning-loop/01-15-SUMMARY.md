---
phase: 01-mod-first-manual-learning-loop
plan: 15
subsystem: ui
tags: [practice, gap-fill, feedback, chip-order]

requires:
  - phase: 01-14
    provides: workspace layout and the open practice shell
provides:
  - per-item chip order seeded by session id and learning unit id
  - visible typed answer, locked grade, stripped sentence, one green blank
  - current pass heading, correct/total score, and plain row labels
  - Start Over on the same first item clears the previous selection
affects: []

actuals:
  tokens: 0
  tasks: 4
  commits: 1

tech-stack:
  added: []
  patterns:
    - chip order is a sha256 Fisher-Yates of the stored span order
    - the renderer key includes the practice session id

key-files:
  created:
    - backend/lait/application/queries/chip_order.py
    - backend/tests/application/test_practice_chip_order.py
    - frontend/src/registries/renderers/stripEmphasis.ts
  modified:
    - backend/lait/application/queries/practice_get.py
    - frontend/src/registries/renderers/GapFillRenderer.tsx
    - frontend/src/registries/renderers/GapFillRenderer.module.css
    - frontend/src/features/lesson/stages/FeedbackStage.tsx
    - frontend/src/features/lesson/FocusPracticeMode.tsx
    - frontend/src/features/lesson/LessonWorkspacePage.tsx

key-decisions:
  - "The stored generation chip list stays in span order. view_for permutes it for the current item."
  - "Start Over remounts the renderer because the key includes sessionId."
  - "The user approved this plan's Docker checkpoint on 2026-10-06. That approval does not close Phase 1."

patterns-established:
  - "Pattern: a new practice session id is part of the gap-fill renderer key"

requirements-completed: []

coverage:
  - id: D1
    description: "Chip order is not the stored span order, survives reload, and changes on Start Over. Drag grading still uses the unit id."
    requirement: EXER-03
    verification:
      - kind: unit
        ref: "backend/tests/application/test_practice_chip_order.py"
        status: pass
      - kind: manual_procedural
        ref: "C:/Users/97255/.codex/visualizations/2026/10/02/01a0fc72-fc87-7723-8dcf-da8bc00ec3f7/LAIT_01-15_BROWSER_REVIEW_2026-10-06.md"
        status: pass
    human_judgment: true
    rationale: "The user approved the Docker checkpoint on 2026-10-06. A real browser-process restart was not performed."
  - id: D2
    description: "The typed answer is visible. A grade disables the chips and the input. The sentence drops emphasis markers and shows one green blank. The current pass shows a score and plain labels."
    requirement: EVAL-05
    verification:
      - kind: automated_ui
        ref: "frontend/src/registries/renderers/gapFillRenderer.test.tsx"
        status: pass
      - kind: automated_ui
        ref: "frontend/src/features/lesson/stages/FeedbackStage.test.tsx"
        status: pass
      - kind: manual_procedural
        ref: "C:/Users/97255/.codex/visualizations/2026/10/02/01a0fc72-fc87-7723-8dcf-da8bc00ec3f7/LAIT_01-15_BROWSER_REVIEW_2026-10-06.md"
        status: pass
    human_judgment: true
    rationale: "The user approved the Docker checkpoint on 2026-10-06 after the Start Over selection fix."

duration: 1d
completed: 2026-10-06
status: complete
---

# Phase 1 Plan 15: Practice and Feedback UX Summary

**A new session shuffles chips without grading by position, the typed answer is visible and locks after a grade, and the current pass reads as a score.**

## Performance

- **Completed:** 2026-10-06
- **Tasks:** 3 implemented, 1 human-verify approved
- **Commits:** 1

## Accomplishments

- `permute_chip_ids` seeds a Fisher-Yates shuffle from the session id and the item id. The generation row stays in span order.
- The typed field has the label Answer, the instruction "Type the missing words.", and a visible border. After a grade the chips and the field are disabled.
- Sentence text drops emphasis markers. The blank is one green line.
- Feedback shows "Current pass", a correct/total score, and Choice, Typed, Correct, Incorrect. The session id is not rendered.
- Start Over on the same first item clears the selected chip. Submit stays disabled until a new choice.

## Task Commits

The implementation and this summary land in one commit on `phase/01-execution`.

## Decisions Made

- Do not rewrite the stored generation on Start Over.
- Do not add a retry button.
- Phase 1 stays open. LESS-01, ANLY-08, and EXER-01 stay Gaps Found.

## Deviations from Plan

- The renderer key did not include the session id, so Start Over on the first question kept `selectedUnitId` and left Submit enabled. The key now starts with `sessionId`. Regression: `clears a selected chip when start over repeats the first item`.

## User Setup Required

None.

## Next Phase Readiness

Plan 01-15 is complete. Phase 1 is not. A real browser-process restart was still a manual item at approval.

## Self-Check: PASSED

- FOUND: backend/lait/application/queries/chip_order.py
- FOUND: frontend/src/registries/renderers/stripEmphasis.ts
- HUMAN: user approved the 01-15 checkpoint
- PHASE: not complete

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-06*
