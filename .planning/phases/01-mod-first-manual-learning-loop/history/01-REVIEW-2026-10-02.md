---
phase: 01-mod-first-manual-learning-loop
reviewed: 2026-10-02T01:10:17Z
depth: standard
files_reviewed: 52
files_reviewed_list:
  - backend/lait/domain/exercise.py
  - backend/lait/domain/learning_unit.py
  - backend/lait/domain/lesson.py
  - backend/lait/domain/practice_session.py
  - backend/lait/domain/span.py
  - backend/lait/application/ports.py
  - backend/lait/application/commands/exercise_generate.py
  - backend/lait/application/commands/exercise_submit_attempt.py
  - backend/lait/application/commands/learning_unit_accept.py
  - backend/lait/application/commands/learning_unit_add.py
  - backend/lait/application/commands/learning_unit_remove.py
  - backend/lait/application/commands/lesson_create.py
  - backend/lait/application/commands/practice_finish.py
  - backend/lait/application/commands/practice_start.py
  - backend/lait/application/commands/practice_start_over.py
  - backend/lait/application/commands/unit_set_freeze.py
  - backend/lait/application/queries/exercise_registry_list_visible.py
  - backend/lait/application/queries/learning_unit_list.py
  - backend/lait/application/queries/lesson_get.py
  - backend/lait/application/queries/lesson_list.py
  - backend/lait/application/queries/module_registry_describe.py
  - backend/lait/application/queries/practice_get.py
  - backend/lait/adapters/http/app.py
  - backend/lait/adapters/http/routers/diagnostics.py
  - backend/lait/adapters/http/routers/exercises.py
  - backend/lait/adapters/http/routers/health.py
  - backend/lait/adapters/http/routers/learning_units.py
  - backend/lait/adapters/http/routers/lessons.py
  - backend/lait/adapters/http/routers/practice.py
  - backend/lait/adapters/persistence/database.py
  - backend/lait/adapters/persistence/lesson_repository.py
  - backend/lait/adapters/persistence/models.py
  - backend/lait/adapters/persistence/repositories.py
  - backend/lait/catalog/loader.py
  - backend/lait/catalog/validation.py
  - backend/lait/modules/exercise_gap_fill/evaluate.py
  - backend/lait/modules/exercise_gap_fill/feedback.py
  - backend/lait/modules/exercise_gap_fill/generate.py
  - backend/lait/modules/exercise_gap_fill/sentence_window.py
  - backend/alembic/versions/20261001_0001_create_lessons.py
  - backend/alembic/versions/20261001_0002_create_learning_units.py
  - backend/alembic/versions/20261001_0003_create_practice_sessions.py
  - frontend/src/features/lesson/LessonWorkspacePage.tsx
  - frontend/src/features/lesson/FocusPracticeMode.tsx
  - frontend/src/features/lesson/lessonApi.ts
  - frontend/src/features/lesson/selectionOffsets.ts
  - frontend/src/features/lesson/stages/LearningUnitsStage.tsx
  - frontend/src/features/lesson/stages/PracticeStage.tsx
  - frontend/src/features/lesson/stages/FeedbackStage.tsx
  - frontend/src/features/lesson/stages/SourceStage.tsx
  - frontend/src/features/lesson/LessonListPage.tsx
  - frontend/src/registries/renderers/GapFillRenderer.tsx
findings:
  critical: 1
  blocker: 1
  warning: 7
  info: 1
  total: 9
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-10-02T01:10:17Z
**Depth:** standard
**Files Reviewed:** 52
**Status:** issues_found

## Summary

The manual loop (lesson, span units, gap-fill generation, one-item submit) is wired, but an open practice session is stored only in React state while the server freeze is keyed by any `open` row. Reload, browser Back, or a double-clicked Start Practice leaves a session id the UI cannot finish, and `practice.start` then reports that session as a stale generation. Unit edits stay rejected with copy that tells the learner to exit a screen they are not on.

Generated clients under `frontend/src/api/generated/**` were secret-scanned only. No embedded credentials and no hand-edit findings.

## Critical Issues

### CR-01: An open practice session the UI no longer holds freezes the lesson permanently

**Classification:** BLOCKER
**File:** `frontend/src/features/lesson/LessonWorkspacePage.tsx:55`
**Issue:** `session` and `focused` live in component state. Nothing writes the session id to the URL, `localStorage`, or a lesson-scoped query. `LessonWorkspacePage` has no unmount or `pagehide` path that calls `practice.finish`. Browser Back, refresh, or closing the tab drops the id while the row stays `open`.

There is no list/resume route. `practice.finish` and `practice.start_over` both require that id. The next `practice.start` treats any open row as a stale generation:

```51:52:backend/lait/application/commands/practice_start.py
    if units.has_open_practice_session(command.lesson_id):
        raise StaleGenerationError(command.lesson_id)
```

The HTTP layer maps that to 409 "Generate exercises again before practice". Generating again does not close the session (`exercise.generate` never checks the freeze). A later Start Practice hits the same 409. The workspace passes `practiceOpen={focused}` (`LessonWorkspacePage.tsx:264`), and `focused` is false on this screen, so the unit stage does not show the lock until a mutation returns 409. `LearningUnitsStage` then sets a sticky lock whose hint is "Exit Practice to edit them" (`LearningUnitsStage.tsx:14`) with no Exit control.

The same brick happens without a reload. `PracticeStage` only disables Start when `enabled` is false (`PracticeStage.tsx:10`). `handleStart` does not set an in-flight flag (`LessonWorkspacePage.tsx:115-126`). Two clicks both pass `has_open_practice_session` because the check and `save_practice_session` are separate transactions, and `practice_sessions` has no unique partial index on `(lesson_id)` where `status = 'open'` (`models.py:83-100`). The UI keeps one id. Exit closes that row. The other stays `open` and the lesson stays frozen.

**Fix:** Persist the open session id per lesson and, on workspace load, resume Focus Practice or call finish. Return the existing open session from `practice.start` instead of `StaleGenerationError`. Make the open-session check and insert one transaction, and add a partial unique index so a second open row cannot commit. Disable Start Practice until the first request settles.

```python
def handle(... ) -> PracticeView:
    existing = units.get_open_practice_session(command.lesson_id)
    if existing is not None:
        generation = units.get_generation(existing.generation_id)
        return view_for(existing, generation)
    # compare accepted ids, then insert in the same transaction as the open check
```

## Warnings

### WR-01: Omitting `target_learning_unit_id` grades the current step with the wrong mode and advances it

**Classification:** WARNING
**File:** `backend/lait/application/commands/exercise_submit_attempt.py:138-154`
**Issue:** `SubmitBody.target_learning_unit_id` is optional. When it is absent, `_resolve_item` returns `practice.items[practice.cursor]` and `advance=True` without comparing `command.kind` to `item.mode`. The handler then builds a `TypedAnswer` or `DragAnswer` from `command.kind` (`exercise_submit_attempt.py:77-89`) and stores `cursor + 1`. A typed body on a drag step is marked by typed string match and consumes the drag step. The targeted path does filter on `item.mode == command.kind`, so the two paths disagree. The shipped client always sends a target, but the server contract does not.

**Fix:** Resolve the current item first, reject the request when `command.kind != item.mode`, and only then build the answer.

```python
item, advance = _resolve_item(practice, command)
if command.kind != item.mode:
    raise NoCurrentItemError(practice.id)
```

### WR-02: `add_attempt` writes a stale cursor over a newer one

**Classification:** WARNING
**File:** `backend/lait/adapters/persistence/repositories.py:251-257`
**Issue:** Submit reads the session, computes `cursor` in memory, then later opens a new transaction and assigns `stored.cursor = cursor`. It does not check that the row is still `open` or that `stored.cursor` is still the snapshot cursor. A slower submit of an earlier item (`advance` is false when `item.position != practice.cursor`, which the API allows via `target_learning_unit_id`) commits the old cursor after a newer submit has moved forward. The pass reopens a step that already has an attempt.

**Fix:** In the same transaction, update the cursor only if the stored status is `open` and the stored cursor still equals the snapshot. Otherwise abort with `NoCurrentItemError`.

```python
if stored.status != OPEN or stored.cursor != expected_cursor:
    raise NoCurrentItemError(attempt.session_id)
stored.cursor = next_cursor
```

### WR-03: A selection anchored on the highlight element is measured as the end of the source

**Classification:** WARNING
**File:** `frontend/src/features/lesson/selectionOffsets.ts:44-62`
**Issue:** `utf16OffsetInRoot` handles an element offset only when `container === root`. Any other element falls through the text walker and returns the sum of all text nodes, which is `source.length`. After a jump, `SourceStage` wraps the span in `<mark id="source-highlight">`. If the browser anchors the range on that `mark` (offset is a child index, not a character index), both ends collapse to the end of the lesson or one end stretches to it. `learning_unit.add` then stores that span. The 422 path below tells the learner it was an overlap, including when the span is actually out of range.

**Fix:** If `container` is an `Element`, resolve the boundary with `container.childNodes[offset]` (or the previous sibling when `offset` is the child count) and continue the text walk from there. Do not return the walked total for an unrecognized container.

### WR-04: Every learning-unit 422 is shown as an overlap

**Classification:** WARNING
**File:** `frontend/src/features/lesson/lessonApi.ts:117-119`
**Issue:** `addLearningUnit` maps every HTTP 422 to `LearningUnitRequestError("overlap")`. The server uses 422 for overlap, for a span outside the source, and for an empty span (`learning_units.py:88-89`). `LearningUnitsStage` always renders "That selection overlaps an existing unit." A bad code-point range is diagnosed as a collision, so the learner retries the same selection.

**Fix:** Read `detail` or a stable `code` (`overlap`, `out_of_range`, `missing_span`) and branch the copy. Keep 409 as the only frozen signal.

### WR-05: Overlap is checked and inserted in two transactions

**Classification:** WARNING
**File:** `backend/lait/application/commands/learning_unit_add.py:54-71`
**Issue:** `list_units` commits its read. `add_unit` inserts in a later transaction. `learning_units` has no exclusion constraint on live spans. Add Learning Unit stays enabled for the whole request (`LearningUnitsStage.tsx:133`), so a double click runs two adds. Both can observe no overlap and both insert. Two live units then share a span. Gap Fill emits two identical chips, and drag grading is by unit id, so one of the two identical chips is scored incorrect.

**Fix:** Take a write transaction, re-read live spans, insert, and commit once. Disable the Add button while the mutation is pending.

### WR-06: `exercise.generate` turns every module exception into a failed generation and drops the error

**Classification:** WARNING
**File:** `backend/lait/application/commands/exercise_generate.py:71-81`
**Issue:** `except Exception` clears definitions and chip ids, then stores `failed` when the tuple is empty. The router returns HTTP 200 with `status: "failed"`. A bug in `generate` (span/text mismatch raises `ValueError` in the gap-fill module) is indistinguishable from "no accepted units", and nothing is logged. Definitions already built for an earlier visible module are discarded with the failure.

**Fix:** Let unexpected exceptions propagate as 500. Catch only the module's declared generation failure, and keep that failure's message on the generation row.

### WR-07: Recorded attempts disappear from the workspace after reload, and the last Continue renders a blank pass

**Classification:** WARNING
**File:** `frontend/src/features/lesson/LessonWorkspacePage.tsx:57`
**Issue:** Attempts are appended only in React state. There is no attempts query. After Exit, refresh resets `attempts` and `feedbackUnlocked`, and `FeedbackStage` renders "No attempts yet" while the rows are still in `attempts`. Separately, `handleContinue` (`LessonWorkspacePage.tsx:150-157`) always refetches. After the last item the server cursor is past the end, `current` is null, and `FocusPracticeMode` renders no exercise and no completion line (`FocusPracticeMode.tsx:42-53`). The session stays `open` until Exit. `handleContinue`, `handleExit`, and `handleStartOver` have no `catch`, so a failed refetch or finish is an unhandled rejection with no alert.

**Fix:** Load attempts for the lesson when the feedback stage opens. When `getPractice` returns `open && current == null`, show a finished state whose primary action calls `practice.finish`. Catch failures and surface them next to the buttons.

## Info

### IN-01: Lesson list failure uses the workspace error copy

**Classification:** INFO
**File:** `frontend/src/features/lesson/LessonListPage.tsx:26-28`
**Issue:** A failed `lesson.list` says "Could not load this lesson. Return to the lesson list and open it again" and links to `/`, which is the page already on screen.
**Fix:** Use list-specific copy, for example "Could not load lessons. Try again."

---

_Reviewed: 2026-10-02T01:10:17Z_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
