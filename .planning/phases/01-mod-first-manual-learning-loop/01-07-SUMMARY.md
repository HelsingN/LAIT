---
phase: 01-mod-first-manual-learning-loop
plan: 07
subsystem: ui
tags: [react, vitest, focus-practice, gap-fill, renderer-registry]

requires:
  - phase: 01-06
    provides: lesson workspace stages and Start Practice gated on the generated accepted set
  - phase: 01-11
    provides: practice.finish and practice.start_over
provides:
  - Focus Practice chrome swap on the lesson route
  - Gap Fill renderer mounted by exercise_type
  - Workspace feedback list of submit responses with excerpt jump
  - Proof renderer registered for the maintainer/test path
affects: [01-08, 01-09]

actuals:
  tokens: 14393
  tasks: 3
  commits: 6
plan_head_before: 0b3ed2efb927a51b67bf6744967d98f90e62162c
plan_head_after: c6d8b6698f78c38a0b15ca00a544063e429e1817

tech-stack:
  added: []
  patterns:
    - Focus Practice replaces lesson chrome on the same route
    - rendererFor(exercise_type) mounts only types present in the learner-visible list
    - Start Over is one call to practice.start_over
    - Attempt rows on the workspace are the submit responses kept in memory

key-files:
  created:
    - frontend/src/features/lesson/FocusPracticeMode.tsx
    - frontend/src/registries/renderers/GapFillRenderer.tsx
    - frontend/src/registries/renderers/ProofRenderer.tsx
    - frontend/src/registries/renderers/registry.ts
    - frontend/src/registries/renderers/types.ts
  modified:
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/lessonApi.ts
    - frontend/src/features/lesson/stages/FeedbackStage.tsx
    - frontend/src/features/lesson/stages/PracticeStage.tsx

key-decisions:
  - "Focus Practice is a chrome swap on /lessons/:id; stage panels stay separate components"
  - "The lesson page mounts rendererFor(exercise_type) only when that type is in the learner-visible list"
  - "Exit Practice calls practice.finish; Start Over calls practice.start_over and does not assemble abandon-plus-start"
  - "Workspace attempt rows are the submit responses kept in memory; Start Over does not clear them"

patterns-established:
  - "Pattern: session navigation stays outside the exercise renderer"
  - "Pattern: the browser displays the submit_attempt category and never sends one"

requirements-completed: [EXER-02, EXER-03, EXER-07, EVAL-01, EVAL-04, EVAL-05, MODL-03]

coverage:
  - id: D1
    description: "Start Practice swaps the lesson route to Focus Practice and wires Submit Answer, Continue, Exit Practice, and confirmed Start Over."
    requirement: EXER-02
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx#submits one typed answer then continues inside the session"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx#exit practice calls finish and restores the workspace"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx#start over confirms then calls start_over only"
        status: pass
    human_judgment: false
  - id: D2
    description: "Gap Fill shows a blanked sentence, drag chips graded by unit id or typed input, Checking…, and one server feedback card."
    requirement: EXER-03
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx#submits a drag chip by unit id and displays the server category"
        status: pass
      - kind: unit
        ref: "frontend/src/registries/renderers/gapFillRenderer.test.tsx#wraps the blank inline and scrolls the chip bank"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx#renders server feedback as text and omits a null natural alternative"
        status: pass
    human_judgment: false
  - id: D3
    description: "After Exit Practice the Feedback stage lists category, explanation, and an excerpt jump. Start Over does not clear those rows."
    requirement: EVAL-05
    verification:
      - kind: unit
        ref: "frontend/src/features/lesson/FeedbackStage.test.tsx#lists category explanation and an excerpt jump"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/FeedbackStage.test.tsx#keeps listed attempts after start over"
        status: pass
      - kind: unit
        ref: "frontend/src/features/lesson/FeedbackStage.test.tsx#shows the empty copy after leaving practice with no attempts"
        status: pass
    human_judgment: false
  - id: D4
    description: "ProofRenderer mounts from the registry by exercise_type in Vitest. Focus Practice does not select it."
    requirement: MODL-03
    verification:
      - kind: unit
        ref: "frontend/src/registries/renderers/proofRenderer.test.ts#mounts the proof renderer by exercise_type"
        status: pass
      - kind: unit
        ref: "frontend/src/registries/renderers/proofRenderer.test.ts#learner focus practice never selects the proof renderer"
        status: pass
    human_judgment: false
  - id: D5
    description: "The Gap Fill sentence wraps, the blank stays inline, and the page does not scroll horizontally at 320px."
    verification: []
    human_judgment: true
    rationale: "Vitest asserts inline blank, overflow-wrap, and overflow-x hidden in CSS. A 320px browser viewport was not opened."

duration: 24min
completed: 2026-10-01
status: complete
---

# Phase 1 Plan 07: Focus Practice Summary

**Focus Practice swaps lesson chrome for a registry-mounted Gap Fill renderer, and the proof renderer mounts only from the test path**

## Performance

- **Duration:** 24 min
- **Started:** 2026-10-01T23:34:00Z
- **Completed:** 2026-10-01T23:58:14Z
- **Tasks:** 3
- **Files modified:** 17

## Accomplishments

- Start Practice hides the stage column and shows the exercise, the frozen-unit hint, and Exit Practice / Start Over. Continue stays in the session. Exit Practice calls `practice.finish`. Start Over confirms, then calls `practice.start_over` only.
- Gap Fill renders the blank inline, uses a chip bank for drag and a text field for typed input, and shows the server category, submitted text, expected text, explanation, and used or missed chunks. A null natural alternative is omitted. Submit does not send a category.
- After leaving practice, Feedback unlocks. Zero attempts show the locked empty copy. Submitted attempts stay listed across Start Over, and the excerpt jump expands the source highlight.
- `rendererFor("proof")` mounts `ProofRenderer` in Vitest. Focus Practice asks the registry only for exercise types returned to the learner.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end Focus Practice submit → feedback → Continue** - `261b2ce` (test, RED) then `c6d8b66` (feat, GREEN)
2. **Task 2: Expand Feedback stage + workspace attempt list** - `e128145` (test, RED) then `60e7421` (feat, GREEN)
3. **Task 3: Proof renderer registry mount** - `c04c724` (test, RED) then `edaf9e9` (feat, GREEN)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `frontend/src/features/lesson/FocusPracticeMode.tsx` - session chrome, learner-list renderer lookup, Start Over confirmation
- `frontend/src/registries/renderers/GapFillRenderer.tsx` - blanked sentence, chips or typed input, Checking…, one feedback card
- `frontend/src/registries/renderers/registry.ts` - `exercise_type` to component map, including proof
- `frontend/src/registries/renderers/ProofRenderer.tsx` - text-only maintainer renderer
- `frontend/src/features/lesson/LessonWorkspacePage.tsx` - chrome swap, practice API calls, attempt list, excerpt jump
- `frontend/src/features/lesson/lessonApi.ts` - start, get, submit, finish, start-over
- `frontend/src/features/lesson/stages/FeedbackStage.tsx` - empty copy or attempt rows
- `frontend/src/features/lesson/stages/PracticeStage.tsx` - Start Practice calls `practice.start`

## Decisions Made

- Focus Practice is the same `/lessons/:id` route with the stage column unmounted. Source, units, generate, practice, and feedback stay separate components.
- The page does not name the Gap Fill module id. It mounts `rendererFor(item.exercise_type)` when that type is in `list_visible_for("learner")`.
- Drag submit sends `kind`, `text`, and `submitted_unit_id`. The card prints the category from the response.
- Attempt rows are accumulated from `exercise.submit_attempt` responses. There is no list endpoint in this plan. Start Over does not clear that array.
- Proof stays registered beside Gap Fill. Removing it later is the catalog entry plus `registerRenderer("proof", ...)` and `ProofRenderer.tsx`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Wired Focus Practice through the lesson page**
- **Found during:** Task 1 (End-to-end Focus Practice submit → feedback → Continue)
- **Issue:** Start Practice lived on `LessonWorkspacePage`, which was not in the task file list. Without that wire the chrome swap never runs.
- **Fix:** The page calls start, submit, get, finish, and start-over, and swaps in `FocusPracticeMode`.
- **Files modified:** `frontend/src/features/lesson/LessonWorkspacePage.tsx`, `frontend/src/features/lesson/lessonApi.ts`
- **Verification:** Focus Practice Vitest file, 6 passed
- **Committed in:** `c6d8b66`

**2. [Rule 2 - Missing Critical] Surface a start failure without leaving the workspace**
- **Found during:** Task 1
- **Issue:** A failed `practice.start` had no UI path. The button would look idle.
- **Fix:** The practice stage shows "Could not start practice. Try again." and stays on the workspace.
- **Files modified:** `frontend/src/features/lesson/LessonWorkspacePage.tsx`
- **Verification:** typecheck; the copy is not on the happy-path tests
- **Committed in:** `c6d8b66`

**3. [Rule 1 - Bug] Excerpt jump used a span that does not contain the unit**
- **Found during:** Task 2 (Expand Feedback stage)
- **Issue:** The RED fixture used start 23 end 34. In this source that slice is `olling out `, so the highlight could not read `rolling out`.
- **Fix:** The fixture span is 22–33, the actual code-point range of `rolling out`.
- **Files modified:** `frontend/src/features/lesson/FeedbackStage.test.tsx`
- **Verification:** `lists category explanation and an excerpt jump` passes
- **Committed in:** `60e7421`

**4. [Rule 3 - Blocking] Focus Practice sources were committed after the proof registration**
- **Found during:** Task 3 close-out
- **Issue:** `FocusPracticeMode`, `GapFillRenderer`, and the practice client edits were still unstaged when the proof commit landed. `60e7421` imports `FocusPracticeMode`, and `edaf9e9` imports `GapFillRenderer`, so those two commits do not build alone.
- **Fix:** `c6d8b66` adds the missing files. Each RED commit still precedes its GREEN commit. HEAD builds.
- **Files modified:** Focus Practice, Gap Fill renderer, `lessonApi.ts`, `PracticeStage.tsx`
- **Verification:** `npx --prefix frontend vitest run src/features/lesson/FocusPracticeMode.test.tsx src/features/lesson/FeedbackStage.test.tsx src/registries/renderers` — 4 files, 12 passed
- **Committed in:** `c6d8b66`

---

**Total deviations:** 4 auto-fixed (1 bug, 1 missing critical, 2 blocking)
**Impact on plan:** The page wire and the late commit are what make the learner path real. No new package, no MCP, and no client-side grade.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 Focus Practice | `261b2ce` `RED_EVIDENCE_OK` / `target_test_failed` for `submits one typed answer then continues inside the session` (exit 1, 7 failed) | `c6d8b66` | — | Pass |
| 2 Feedback list | `e128145` `RED_EVIDENCE_OK` / `target_test_failed` for `lists category explanation and an excerpt jump` (exit 1, 3 failed) | `60e7421` | — | Pass |
| 3 Proof mount | `c04c724` `RED_EVIDENCE_OK` / `target_test_failed` for `mounts the proof renderer by exercise_type` (exit 1, 1 failed) | `edaf9e9` | — | Pass |

## Authentication Gates

None.

## Issues Encountered

None in the plan tests. `npx --prefix frontend vitest run src/features/lesson` — 5 files, 30 passed. `npm --prefix frontend run typecheck` passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for the remaining phase 01 plans. The learner can enter Focus Practice from a completed generation, submit Gap Fill, and leave a durable in-memory attempt list.
- Attempt history does not survive a reload. A list query was outside this plan's files.
- MODL-03 is also declared by plan 01-09, so that requirement stays open until 01-09 has a summary.
- `main` was not moved.

## Self-Check: PASSED

- FOUND: `frontend/src/features/lesson/FocusPracticeMode.tsx`
- FOUND: `frontend/src/registries/renderers/GapFillRenderer.tsx`
- FOUND: `frontend/src/registries/renderers/ProofRenderer.tsx`
- FOUND: `frontend/src/registries/renderers/registry.ts`
- FOUND: `261b2ce`
- FOUND: `c6d8b66`
- FOUND: `e128145`
- FOUND: `60e7421`
- FOUND: `c04c724`
- FOUND: `edaf9e9`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
