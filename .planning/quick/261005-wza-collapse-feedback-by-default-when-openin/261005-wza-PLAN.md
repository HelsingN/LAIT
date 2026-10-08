---
quick_id: 261005-wza
autonomous: false
files_modified:
  - frontend/src/features/lesson/LessonWorkspacePage.tsx
  - frontend/src/features/lesson/LessonWorkspacePage.test.tsx
---

# Feedback collapsed on lesson entry

Use gsd-quick inline on the current branch. No commit/push; preserve the active UAT and Phase 1 status.

<threat_model>
UI-state-only change, ASVS level 1. No transport, database, authentication, or external integration changes. Preserve attempt data; exercise/practice mutations are not used for verification.
</threat_model>

<task type="auto">
  <name>Collapse Feedback on entry and retain new-practice results</name>
  <files>frontend/src/features/lesson/LessonWorkspacePage.tsx, frontend/src/features/lesson/LessonWorkspacePage.test.tsx</files>
  <action>Ignore saved Feedback expansion on mount, remove auto-expansion during history hydration, retain manual toggling and automatic expansion after practice finish/exit. Add regression tests for old saved state, remount/reload and manual history disclosure; update short-window cover test to open Feedback explicitly.</action>
  <verify><automated>npm --prefix frontend test; npm --prefix frontend run typecheck</automated></verify>
  <done>Feedback stays collapsed when saved history arrives; existing practice-result tests remain green.</done>
</task>

<task type="checkpoint:human-verify" gate="blocking-human">
  <what-built>Feedback starts collapsed even when it was previously open. History remains accessible and new practice results still open automatically.</what-built>
  <how-to-verify>On Compose port 5173, hard-reload the lesson, open Feedback manually, reload, and return through Lessons. Each entry starts collapsed; disclosure shows the saved history. A new browser session and recreated web container use the same default. Database/API are unchanged; no separate API restart required. Practice finish/exit still opens its result. Rebuild only web, retaining volumes.</how-to-verify>
  <resume-signal>Reply approved or describe observations. Tests do not approve the checkpoint.</resume-signal>
</task>
