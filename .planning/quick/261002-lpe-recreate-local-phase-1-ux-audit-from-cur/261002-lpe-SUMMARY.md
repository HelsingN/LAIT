---
quick_id: 261002-lpe
date: 2026-10-02
status: complete
---

# Local UX audit reconstructed

Created docs/audits/PHASE1_UX_AUDIT_2026-10-02.md with six findings from the current conversation, proposed remedies clearly separate from observations, and explicit limits on functional verification and historical bug reports.

Preserved four user screenshots under docs/audits/evidence/2026-10-02. Evidence links and local file presence checked after installation. Added a quick-task completion entry to STATE.md while preserving existing phase state and user edits.

Executed inline. No application changes, staging, commits, or pushes; the user's no-commit instruction overrides the workflow commit steps. No phase-close approval implied.

## Documentation continuation — 2026-10-04

Resumed this audit-documentation task inline to record the second 01-14 checkpoint on the rebuilt Compose web app. Added UX-18 (intrinsic-sized preparation causes Add/units to leave the visible preparation viewport) and UX-19 (open Feedback leaves only 8px of preparation at 1280×520), exact measurements, three screenshot references, passed interactions and explicit test limitations. Earlier content is preserved.

The user authorized two temporary draft units; both were created and removed through the UI, one with the mouse and one with the keyboard. Original three units and visible ready state were restored after reload and return from Lessons. No Accept, Generate, practice submission, or Docker restart performed.

This continuation updates only the audit, its evidence, and this quick summary. The existing STATE quick-task entry is retained; no duplicate task, phase-plan changes, approval, phase transition, commit, or push. A full-phase gsd-verify-work sealing workflow was not launched for this scoped checkpoint. Windows/browser 125% scaling and cache-bypassing hard reload remain unverified.

## Documentation continuation after feedbackCover — 2026-10-04

Resumed the same quick task inline; no new quick directory or duplicate STATE row. Recorded the current rebuilt Compose checkpoint: UX-18/UX-19 no longer reproduce in the checked dimensions; Source/list scroll independently, Add remains in view, and low-window Feedback covers preparation while preserving scroll and selection. Added UX-20: at 1280×800 with real history open, Exercises shrinks to about 9px and clips its heading/ready text. Added three screenshots and explicit viewport/scale/threshold/cache limitations, preserving all earlier audit content including intervening Cursor updates.

With explicit user permission, created and removed two disposable drafts (one mouse, one keyboard); did not Accept either. Original three phrases remain after reload and return from Lessons. No Generate, Start Practice, answer submission, Docker restart, application changes, plan edits, commit, push or checkpoint approval. Only audit/evidence and this summary updated; GSD manual checkpoint remains user-controlled.

## Documentation continuation confirming UX-20 fix — 2026-10-04

Recorded three passing browser scenarios on the rebuilt Compose app: 1280×800 Exercises remains 112px with heading/type/ready fully visible while Feedback scrolls within 266px; 1280×520 Feedback covers the preparation slot at 188px and closing restores Source/list scroll plus selected unit; 959×700 shows Add, two whole unit rows and Start without preparation/page overflow. UX-20 no longer reproduces in these conditions. Added three current screenshots; preserved previous findings and intervening implementer notes.

No lesson data mutations in this recheck, no new quick task/STATE row, application or plan changes, automated test run, commit, push, phase transition or user approval. CSS viewport measurements verified; physical Windows 125% scaling and cache bypass remain unverified. Only the existing audit/evidence and this quick summary updated. Checkpoint 01-14 remains awaiting the human user's decision.

## Documentation continuation — tooltip proposal, 2026-10-05

Recorded UX-21 from the user's screenshot and request: replace the persistent truncated Add Learning Unit hint with a non-layout-shifting tooltip while the button is inactive. Captured hover/focus accessibility, disabled-action protection and proposed verification criteria, clearly separate from implemented/tested behavior. Preserved the user's reported approved checkpoint 01-14 and open Phase 1; this minor follow-up does not reopen approval or start the practice/Feedback slice.

Only audit, supplied screenshot evidence and this existing quick summary updated inline. No application changes, new quick task/STATE row, phase-plan changes, approval transition, commit or push.
