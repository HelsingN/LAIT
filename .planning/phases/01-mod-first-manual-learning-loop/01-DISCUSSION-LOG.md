# Phase 1: Mod-First Manual Learning Loop - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-28
**Phase:** 1-Mod-First Manual Learning Loop
**Areas discussed:** Learner path and screens, Manual learning-unit capture, Gap Fill practice and feedback, Mod-First proof surface, Sentence blanks and session restart

---

## Learner path and screens

Carried forward from the interrupted checkpoint. Not re-litigated in this session.

**User's choice:** Lesson workspace with staged panels and a separate Focus Practice Mode.
**Notes:** Lesson List is only the entry point. Title is suggested from the first meaningful line, otherwise `Untitled Lesson`, with an immutable internal id. Source excerpts jump to the full source. Ending practice restores the workspace.

---

## Manual learning-unit capture

| Option | Description | Selected |
|--------|-------------|----------|
| Selection-first | Highlight a span. That span is the unit text and the occurrence. | |
| Selection or free text | Type a unit with an optional span. | |
| Card | Target plus required gloss and example sentence. | |
| You decide | Agent would have locked selection-first. | |

**User's choice:** First reply was option 4 plus "paste txt/md, free input, LLM later". The user then said that answer misunderstood what a unit is. Corrected choice: selection only, plus an explicit Add button. LLM generation of units comes later.
**Notes:** The txt/md and free-input reply was discarded. Add does nothing without a selection. Unit text is exactly the span and is not editable in this phase.

| Option | Description | Selected |
|--------|-------------|----------|
| One button, immediately accepted | Add creates an accepted unit. | |
| Two buttons | Add stores a draft. Accept makes it eligible for Gap Fill. | ✓ |
| You decide | Agent would have picked immediate accept. | |

**User's choice:** Two buttons.
**Notes:** Drafts cannot generate exercises.

| Option | Description | Selected |
|--------|-------------|----------|
| Add and Accept only | No delete. | |
| Delete draft, unaccept until generation | Limited undo. | |
| Delete any time | Including after generation. | |
| You decide | Agent would have picked delete-until-generation. | |

**User's choice:** Before practice, add, delete, and re-add. The only extra constraint is that unit spans must not overlap.
**Notes:** Touching edges are allowed. The same phrase in two places is two units. An overlapping selection is rejected.

| Option | Description | Selected |
|--------|-------------|----------|
| Freeze at Practice start | Change the set only by leaving the session. | ✓ |
| Freeze at Generate Exercises | Frozen once exercises exist. | |
| Freeze at first Submit | Editable until the first answer. | |
| You decide | Agent would have picked Practice start. | |

**User's choice:** Option 1. To change units, finish/close the lesson or start over.
**Notes:** Later refined under "Start over": close returns to the workspace and unfreezes units. Start over abandons the session and opens a new one on the same set.

---

## Gap Fill practice and feedback

| Option | Description | Selected |
|--------|-------------|----------|
| Type the blank | Learner types the unit. | |
| Choose from options | Multiple choice. | |
| You decide | Agent would have picked typing because Phase 1 has no distractor generator. | |

**User's choice:** Depends on the exercise type: drag from a set, or manual input. Then clarified for Gap Fill itself.
**Notes:** Simple Gap Fill is drag-and-drop of answer options. Harder Gap Fill is manual input. Both modes are Phase 1 `exercise-gap-fill`, not later exercise types.

| Option | Description | Selected |
|--------|-------------|----------|
| Other accepted units | Chips are the correct unit plus other accepted units of the lesson. One unit means no drag pass. | ✓ |
| Other pieces of the same sentence | Chips cut from the sentence. | |
| You decide | Agent would have picked other accepted units. | |

**User's choice:** Option 1.

| Option | Description | Selected |
|--------|-------------|----------|
| Two items per unit | Drag, then immediately type the same blank. | |
| Two passes | All units dragged, then all units typed. | ✓ |
| One mode per session | Learner picks drag or type before practice. | |
| You decide | Agent would have picked two items per unit. | |

**User's choice:** Option 2.

| Option | Description | Selected |
|--------|-------------|----------|
| Exact characters | `Rolling out` is incorrect for `rolling out`. | |
| Trim and case | Trim the ends and ignore case. Internal space, period, or apostrophe still fails. | ✓ |
| Full English rules now | Pull EVAL-02 into Phase 1. | |
| You decide | Agent would have picked trim and case. | |

**User's choice:** Option 2.
**Notes:** Phase 1 categories for Gap Fill are only `correct` and `incorrect`.

---

## Mod-First proof surface

| Option | Description | Selected |
|--------|-------------|----------|
| Maintainer and tests only | Proof module is registered but absent from the learner workflow. | ✓ |
| Off by default | Maintainer can enable it on a lesson. | |
| Always in the session | Learner sees Gap Fill and the proof exercise together. | |
| You decide | Agent would have picked maintainer and tests only. | |

**User's choice:** Option 1. Same public contracts, static catalog, and renderer registry as Gap Fill. Proof of success is removing the proof module from the catalog with no Core changes while LAIT keeps working.
**Notes:** Learner workflow in Phase 1 stays Gap Fill only.

| Option | Description | Selected |
|--------|-------------|----------|
| Catalog flag `learnerVisible` | Lesson UI filters the registry. | refined |
| Lesson UI knows the Gap Fill id | Screen never asks the registry for all exercises. | |
| You decide | Agent would have picked the boolean flag. | |

**User's choice:** Option 1, but `visibility: learner | maintainer` on the exercise contribution, not a boolean and not a field of the universal module manifest. The lesson UI calls `listExercises()` and keeps `visibility == learner`. It must not know the Gap Fill id.
**Notes:** `experimental` is a later enum value. Maintainer and tests can read the whole registry.

| Option | Description | Selected |
|--------|-------------|----------|
| Documented diagnostic query only | No maintainer page. | ✓ |
| Separate maintainer route | Same public fields, hidden from the lesson nav. | |
| You decide | Agent would have picked the query. | |

**User's choice:** Option 1. Learner list and maintainer diagnostics are different operations: `exercise_registry.list_visible_for("learner")` and `module_registry.describe()`. The lesson UI must not call the diagnostic query.
**Notes:** Acceptance includes seeing both modules activated by one public mechanism while proof stays out of the learner workflow.

| Option | Description | Selected |
|--------|-------------|----------|
| Whole learner scenario as commands | UI calls the command boundary. | refined |
| Diagnostics only | Lesson flow calls services from HTTP handlers. | |
| You decide | Agent would have picked the command boundary. | |

**User's choice:** Option 1, clarified: state changes are commands, reads are queries, HTTP is only an adapter. In-process typed handlers, not a distributed command bus. Acceptance: a future MCP adapter can replace the FastAPI router without changing Core, the application workflow, or exercise modules.
**Notes:** `lesson.list` was in the first query list and omitted in the second paste. It was kept because LESS-02 requires a lesson list. The user did not strike it when accepting the summary.

---

## Sentence blanks, order, feedback copy, restart

The user answered four follow-up gray areas in one message.

**User's choice:**
- Hide only the current target span. Neighboring units stay visible.
- Order by source position, tie-break `learning_unit_id`, not Accept order.
- Explanation is a required deterministic template. Natural alternative is optional and nullable.
- Start over abandons the current session and creates a new one. Recorded attempts are never deleted. Only not-yet-submitted state disappears.

**Notes:** Close-to-workspace still unfreezes units. Start over does not.

---

## Claude's Discretion

- How start-over is spelled as commands, as long as it abandons the open session, opens a new one, does not unfreeze units, and does not delete attempts.
- The smallest contract-valid body of the proof exercise, as long as it stays off the learner list and mounts through maintainer/test paths.

## Deferred Ideas

- Full Workspace API and dockable layouts, around Phases 6–8.
- Session modes Classic, Exam, Game, and Reading.
- LLM unit generation (Phase 2) and unit-text editing (Phase 2).
- `visibility: experimental` and a maintainer diagnostics page.
- EVAL-02 normalization and richer grammar explanations.
- MCP adapter implementation. The boundary is in scope. The adapter is not.
- Retry, reveal, and session resume.
