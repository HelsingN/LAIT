---
quick_id: 261005-wza
status: complete
checkpoint: approved
commits: 0
---

# Feedback collapsed on lesson entry

Implementation and blocking-human checkpoint complete. The user confirmed: "Ручной checkpoint пройден" on 2026-10-05. This approval applies only to quick task 261005-wza; Phase 1 and the existing UAT session are not approved or completed by it.

- LessonWorkspacePage starts with Feedback collapsed, ignoring its previous saved expansion while retaining other stage preferences.
- Loading saved attempts unlocks Feedback without expanding it. Manual disclosure still displays history.
- Newly completed/exited practice still expands its result through revealPass; existing completion/exit/recovery tests remain green.
- Added two regression cases for saved true/false state, manual disclosure and reopening; adapted history restoration and short-window cover tests to open Feedback explicitly.

Verification: 9 frontend test files, 56/56 tests passed; TypeScript check passed. Compose web rebuilt and recreated using --no-deps. Served lesson route returned HTTP 200 with new index-lJFO54jp.js. API container id stayed 65a287c7d9ed, healthy; lait_app-data retained. Backend code and data untouched.

Workflow: gsd-quick executed inline without subagents. Commits intentionally omitted per user workflow. GSD's quick-tasks-append created the schema-safe STATE row; its automatic HEAD cell was corrected to Uncommitted because HEAD is not a commit for this change.

Human verification: passed, as reported by the user. The checkpoint covered collapsed Feedback on lesson entry, manual history disclosure and reopening, with practice-result disclosure preserved. No new test or application mutation was run while recording approval. No commit or push was made.
