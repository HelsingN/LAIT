# UX-16 / UX-17 diagnosis

Date: 2026-10-02. Branch: `phase/01-execution`. No production code changed.

Source: `docs/audits/PHASE1_UX_AUDIT_2026-10-02.md`. Lesson `8530f437-cf76-42ed-a835-b6782381cc26`.

## UX-16 — reload drops Feedback and practice readiness

The rows are still in SQLite. The workspace never reads them.

Observed in `/app/data/lait.db` on the running Compose volume (read-only): source length 1749, 4 live units, 9 `completed` generations with the same accepted-unit id set, 7 practice sessions, 21 attempts. The full pass `2e60eb0e-b9fa-4d53-a525-49e4ac1bd936` is `closed`, cursor 8, four `drag` and four `typed`, all `correct`.

`LessonWorkspacePage` keeps `generation`, `practiceUnlocked`, `attempts`, and `feedbackUnlocked` in React state. Reload mounts them empty. `practiceUnlocked` becomes true only in the generate mutation `onSuccess`. `feedbackUnlocked` becomes true only in `handleExit`. `StageSection` renders a panel only when `unlocked && expanded`, so a stored expansion cannot show Practice or Feedback.

`handleExit` calls `practice.finish` and `clearOpenPracticeSessionId`. After that, load has no session id. `practice.get` would not return attempts anyway: `view_for` builds only the current item. There is no lesson-scoped read for the latest completed generation or for attempts. Opening the lesson calls `lesson.get` and `learning_unit.list` only. A later Generate creates another `completed` row for the same accepted set.

## UX-17 — last Continue leaves an empty Focus Practice

`exercise.submit_attempt` advances `cursor` and returns `session_open=True`. Only `practice.finish` sets `closed`. Four units produce eight pass items. After the eighth submit, cursor is 8. `practice.get` then returns `open: true` and `current: null` because `cursor < len(items)` is false. `handleContinue` stores that view and leaves `focused` true. `FocusPracticeMode` mounts no renderer when `item` is null, so the frozen hint, Exit, and Start Over remain.

The row is `closed` with cursor 8 only because Exit was pressed afterwards. The empty screen happened while the session was still open.

## Not in this diagnosis

Slices 2–4 (layout, chip order, feedback card redesign, drag and drop, retry, resume-after-exit) stay out of scope. Retry after an incorrect answer and continuing a closed session are not approved requirements.
