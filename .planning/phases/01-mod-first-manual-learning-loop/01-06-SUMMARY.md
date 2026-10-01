---
phase: 01-mod-first-manual-learning-loop
plan: 06
subsystem: ui
tags: [react, vitest, lesson-workspace, unicode-offsets, learning-units]

requires:
  - phase: 01-01
    provides: lesson list, create form, self-hosted WOFF2, design tokens
  - phase: 01-05
    provides: exercise.generate and the accepted-unit id set that practice.start checks
provides:
  - Lesson workspace stage shell from Source through Feedback
  - Manual unit add, accept, and delete with Unicode code-point spans
  - Generate Exercises pending and terminal copy, with Start Practice gated on that accepted set
  - Lesson list and create copy states, including a two-line title field
affects: [01-07, 01-08]

actuals:
  tokens: 28719
  tasks: 3
  commits: 5
plan_head_before: a30888393aeb85e4168fc96f19c6ce03860aa375
plan_head_after: 18b4a3e0fa3b6c79f080713be41c10b837a773a2

tech-stack:
  added: [vitest, @testing-library/react, @testing-library/user-event, @testing-library/jest-dom, jsdom]
  patterns:
    - stage expansion persisted per lesson id in localStorage
    - DOM UTF-16 selection offsets converted to Unicode code points before learning_unit.add
    - learner exercise types loaded from list_visible_for, never describe()

key-files:
  created:
    - frontend/src/features/lesson/lessonApi.ts
    - frontend/src/features/lesson/stageState.ts
    - frontend/src/features/lesson/selectionOffsets.ts
    - frontend/src/features/lesson/CreateLessonForm.tsx
    - frontend/src/features/lesson/stages/SourceStage.tsx
    - frontend/src/features/lesson/stages/LearningUnitsStage.tsx
    - frontend/src/features/lesson/stages/GenerateExercisesStage.tsx
    - frontend/src/features/lesson/stages/PracticeStage.tsx
    - frontend/src/features/lesson/stages/FeedbackStage.tsx
  modified:
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/LessonListPage.tsx

key-decisions:
  - "The workspace always mounts Source, Learning Units, Generate Exercises, Practice, and Feedback. Loading and load errors render inside the open stage."
  - "learning_unit.add posts Unicode code points only. Selecting out in 👍out sends start 1 and end 4."
  - "Start Practice enables only after generate returns completed for the current accepted-unit id set. A draft-only add does not disable it."
  - "Learner exercise types come from GET /api/exercise-registry?visibility=learner. The lesson UI does not call describe()."
  - "The create title control is a two-line textarea. A blank title still stores Untitled Lesson."

patterns-established:
  - "Pattern: stage chrome reads list_visible_for and renders exercise_type, not a module id"
  - "Pattern: selection code points are computed from the source text node before POST"
  - "Pattern: Practice in this plan is the Start Practice affordance; Focus Practice Mode is plan 01-07"

requirements-completed: [LESS-01, LESS-02, ANLY-08, EXER-01]

coverage:
  - id: D1
    description: "Lesson workspace is a stage shell. Loading and load errors stay inside the stage column, and the column and source body scroll vertically."
    requirement: LESS-02
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#shell-has-no-outer-empty-loading-error"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#stage-column-scroll-fixed-labels"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#source-panel-body-scrolls"
        status: pass
    human_judgment: false
  - id: D2
    description: "Add Learning Unit posts Unicode code points. A selection of out after U+1F44D sends start 1 and end 4."
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LearningUnitsStage.test.tsx#converts a selection after an emoji to Unicode code points"
        status: pass
    human_judgment: false
  - id: D3
    description: "Generate Exercises shows Generating… then completed or the locked failure copy. Start Practice stays disabled until that generation matches the current accepted set."
    requirement: EXER-01
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#shows Generating… then the no-accepted failure copy"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#enables Start Practice only for the generated accepted set"
        status: pass
    human_judgment: false
  - id: D4
    description: "Lesson list and create use the locked empty, loading, error, Untitled Lesson, and Creating… copy. The title field wraps to two lines."
    requirement: LESS-01
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LessonListPage.test.tsx#shows the empty lesson list copy and Create Lesson"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/LessonListPage.test.tsx#suggests Untitled Lesson and wraps the title field to two lines"
        status: pass
    human_judgment: false
  - id: D5
    description: "Lesson UI does not call module_registry.describe or hard-code the Gap Fill module id."
    requirement: EXER-01
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx#does not reference module_registry.describe in lesson feature source"
        status: pass
    human_judgment: false

duration: 10h 1m
completed: 2026-10-01
status: complete
---

# Phase 1 Plan 06: Lesson Workspace Stages Summary

**Lesson workspace stages from Source through Generate Exercises, with Unicode code-point unit spans and Start Practice gated on the generated accepted set**

## Performance

- **Duration:** 10h 1m
- **Started:** 2026-10-01T10:37:38Z
- **Completed:** 2026-10-01T20:38:30Z
- **Tasks:** 3
- **Files modified:** 23

## Accomplishments

- The lesson route is a five-stage shell. Loading and load errors stay inside the open stage, the stage column scrolls, and the source body scrolls without injecting HTML.
- Add Learning Unit converts DOM UTF-16 offsets to Unicode code points. Selecting `out` in `👍out` posts `start: 1` and `end: 4`.
- Generate Exercises shows `Generating…`, then `completed` or the locked failure copy. Start Practice enables only when that completed set still matches the accepted units. A draft-only add leaves it enabled.
- Lesson list and create keep the locked empty, loading, error, `Untitled Lesson`, and `Creating…` strings. The title field is a two-line textarea.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end UI paste → units → generate status** - `631e951` (test), `65a457e` (feat)
2. **Task 2: Expand Learning Units interaction tests** - `30d3668` (test)
3. **Task 3: Expand list/create UI-SPEC copy states** - `98b73f1` (test), `18b4a3e` (feat)

**Plan metadata:** pending docs commit

## Files Created/Modified

- `frontend/src/features/lesson/LessonWorkspacePage.tsx` - stage shell, generation snapshot, Start Practice gate
- `frontend/src/features/lesson/stages/SourceStage.tsx` - read-only scrolling source and selection reporting
- `frontend/src/features/lesson/stages/LearningUnitsStage.tsx` - add, accept, delete, overlap copy, frozen hint
- `frontend/src/features/lesson/stages/GenerateExercisesStage.tsx` - pending and terminal generate copy plus learner exercise types
- `frontend/src/features/lesson/stages/PracticeStage.tsx` - Start Practice affordance only
- `frontend/src/features/lesson/selectionOffsets.ts` - UTF-16 selection offsets to Unicode code points
- `frontend/src/features/lesson/lessonApi.ts` - hand-written client for lesson, unit, registry, and generate calls
- `frontend/src/features/lesson/CreateLessonForm.tsx` - paste form with a two-line title field
- `frontend/src/features/lesson/stageState.ts` - per-lesson expand/collapse in localStorage

## Decisions Made

- The shell is navigation. It does not replace itself with a page-level empty, loading, or error view.
- `learning_unit.add` sends `{ start, end }` code points and no unit text.
- Start Practice compares the completed generation's `accepted_unit_ids` with the current accepted ids. Accepting or deleting an accepted unit disables it until Generate Exercises succeeds again.
- Exercise type labels are the `exercise_type` values from `GET /api/exercise-registry?visibility=learner`.
- Clicking Start Practice, Focus Practice Mode, and the Feedback attempt list stay on plan 01-07. This plan only shows the disabled or enabled button.
- Fonts stay the WOFF2 files from plan 01-01. No font CDN and no second font package.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added the Vitest runner the plan's verify commands call**
- **Found during:** Task 1 (End-to-end UI paste → units → generate status)
- **Issue:** `frontend/package.json` had no test runner, and `npx --prefix frontend vitest` executes with the repo root as cwd, so it does not load `frontend/vite.config.ts`.
- **Fix:** Installed Vitest 5.0.3, Testing Library, and jsdom. Marked the lesson tests with `@vitest-environment jsdom` so the plan command gets a document.
- **Files modified:** `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.app.json`, lesson test files
- **Verification:** `npx --prefix frontend vitest run src/features/lesson` — 3 files, 21 passed
- **Committed in:** `631e951` (test infra) and `65a457e` (jsdom docblock)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** The test runner was required to execute the plan's verify commands. No product scope was added.

## TDD Gate Compliance

| Task | RED | GREEN | Status |
|------|-----|-------|--------|
| 1 workspace shell | `631e951` failed on missing stage labels | `65a457e` | Pass |
| 2 unit interactions | `30d3668` passed on first run | behavior already in `65a457e` | Advisory |
| 3 list/create title wrap | `98b73f1` failed because the title control was an `INPUT` | `18b4a3e` | Pass |

Task 2 is advisory. The tracer task required a production-quality code-point conversion, overlap copy, empty state, and frozen hint before the expansion tests. Those tests, including `converts a selection after an emoji to Unicode code points`, passed on the first run. There is no separate failing commit for that file.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for plan 01-07 to enter Focus Practice Mode from the enabled Start Practice button and to fill the Feedback stage after attempts exist.
- The hand-written `lessonApi.ts` still matches the current handler DTOs and is the swap point for the generated client in plan 01-08.

## Self-Check: PASSED

- FOUND: `frontend/src/features/lesson/LessonWorkspacePage.tsx`
- FOUND: `frontend/src/features/lesson/stages/LearningUnitsStage.tsx`
- FOUND: `frontend/src/features/lesson/stages/GenerateExercisesStage.tsx`
- FOUND: `frontend/src/features/lesson/LearningUnitsStage.test.tsx`
- FOUND: `631e951`
- FOUND: `65a457e`
- FOUND: `30d3668`
- FOUND: `98b73f1`
- FOUND: `18b4a3e`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
