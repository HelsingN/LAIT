---
phase: 01-mod-first-manual-learning-loop
plan: 18
revision: 2
status: approved
checkpoint_task: 3
gate: blocking-human
completed_automatic_tasks: [1, 2]
human_approval: approved
approval_date: 2026-10-07
approval_source: user_report
commits: 0
---

# 01-18 R2 — repeated Docker checkpoint: inline result

Latest authority: 01-18-CONTEXT.md D-32–D-37, agreed 2026-10-07 after the user explicitly said **not approved**. R1 is archived in 01-18-CHECKPOINT-R1.md, not passed. The repeated sole final T3 checkpoint is now approved by the user's report; this completes plan 01-18, not Phase 1.

## What is built

- Correct/Corrected fills the current blank with the accepted reference phrase once in green; category text stays visible. No separate answer card, duplicate graded input or chip bank.
- Incorrect puts only submitted text inline. Show answer fills the reference but leaves Incorrect unchanged. Try again is available before and after reveal, clears blank/result, and permits another submission for the same item.
- No Details, Chunks used/missed labels, detailed teaching/alternative display, LLM or new explanation template in this revision. Original **full EVAL-05 remains incomplete**: Phase 1 is explicitly narrowed; remaining education is recorded in 01-18-FOLLOWUPS.md (Phase 5 feedback follow-up).
- All 01-17/01-18 durable payload, identity/snapshot/reveal and async-guard fixes remain. Real explanation/chunks/nullable alternative still arrive at the renderer seam and stay recoverable through public reads; no []/null substitutes or saved-content rewriting.
- Same-session retries, corrected exclusion, opening score, Continue, Start Over and Exit stay unchanged. Shared multi-blank exercise and actual drag-and-drop are recorded only as proposed Phase 4/9 follow-ups.

The legacy test id feedback-card now identifies the whole result-bearing exercise root; no visual answer card or article remains. This is test compatibility, not a learner-visible label.

## Automatic evidence — current R2, not human approval

| Check | Result |
| --- | --- |
| Renderer new RED before production edit | 10 failed / 6 passed; missing inline answers, old Details, no post-reveal Try again. One failure also exposed event argument forwarding; it was fixed with a parameterless retry wrapper. |
| Renderer GREEN, then tracer rerun | 16 passed each run |
| Workspace + FocusPracticeMode + stages/FeedbackStage | 69 passed; includes 59 workspace cases with new hidden/revealed saved Try again tests |
| Full frontend | 105 passed, 9 files |
| Full backend | 129 passed, no skipped; pre-existing Starlette/httpx deprecation warning only |
| npm --prefix frontend run typecheck / build | Passed; production index-I9J8SvOc.js + index-D6b_DoN8.css |
| Revised plan frontmatter / plan structure | Valid; 3 tasks, no errors/warnings, one final blocking-human task |
| Decision coverage D-32–D-37 / failure directions | 6/6 decisions covered; all 6 current automated commands state failure conditions |
| UI safety gate | UI-SPEC exists, no block |

Commands: node frontend/node_modules/vitest/vitest.mjs run --root frontend [target files or full suite] --maxWorkers=1; .venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests -q. Exact executable commands are in revised 01-18-PLAN.md.

Rich restored payload is asserted through a real FocusPracticeMode props spy (including exact old explanation and non-null alternative), even though these fields are deliberately no longer displayed. Existing malformed/missing-history, retry-copy, stale-reveal, retained-callback, late-submit/get/list, final-success and frozen queue/score/Exit cases remain. T2 is a test-contract revision of retained production restore; no new T2 production mechanism or invented RED/commit evidence.

## Docker/data preservation

docker compose up -d --build --wait api web and docker compose restart api web succeeded with the existing volume kept. API health is ok; web http://127.0.0.1:5173 returns HTTP 200 and matching JS/CSS. The updated web image is 619c8cdef75a0787048cce6056417f24e8d325b56422160a09e52135559cd360; API image unchanged.

This revision captured its own read-only baseline after the user's earlier testing: **1 lesson / 188 attempts** (not the old R1 181). Before rebuild/restart and after restart, all full attempt payloads were identical, including 152 nonempty used arrays, 36 nonempty missed arrays and genuinely null alternatives:

E6E8B582FB72B561867F3E3C6844E75D40AA3CD7BDE58DFB93130205D5F70B6B

Digest procedure is unchanged: GET /api/lessons .lessons → GET each /attempts .attempts → sort attempt_id → ConvertTo-Json -Depth 30 -Compress → SHA256 UTF-8. No user-data writes, SQL edits, seeding or volume deletion. Automatic payload equality proves data preservation, **not** human-visible state restoration.

Manual non-null-alternative display is no longer a Phase 1 acceptance row: display was explicitly deferred, not passed. Rich non-null persistence/restore remains automatically checked. Backend and restore production code were not changed by this revision.

## T3 — approved human verification checklist

On 2026-10-07 the user reported: “ручная проверка пройдена без замечаний approved.” This approves the published R2 checklist as a whole. The matrix below records user-reported passes, not assistant-observed browser actions; no per-route logs or screenshots were supplied. No observations were reported to classify. R1 remains not approved.

Use **http://127.0.0.1:5173**, same origin/profile throughout. Docker images are current. A dev server, green tests or a new tab do not approve this gate.

1. Submit a wrong typed response: it appears once in the blank, Incorrect is visible, reference stays hidden; no Details/chunk labels or duplicate graded input/card.
2. Show answer: accepted reference replaces the wrong text in the blank, Incorrect remains, no new attempt/cursor/score change. Try again then clears blank/result and restores empty entry; also test Try again before reveal.
3. Produce Correct and Corrected: accepted reference is green and shown once in context; no duplicate input/chips/card. Check long phrase wrap at 320px and visible result text, not color alone.
4. For **each state**, test **each route separately**, before Continue for correct/corrected; include a final success with server cursor exhausted:

| State | Reload | Direct lesson URL | Lesson List return | Fully quit/relaunch browser process | Docker/app restart, volume kept |
| --- | --- | --- | --- | --- | --- |
| Incorrect hidden | pass (user report) | pass (user report) | pass (user report) | pass (user report) | pass (user report) |
| Same incorrect attempt after Show answer | pass (user report) | pass (user report) | pass (user report) | pass (user report) | pass (user report) |
| Correct before Continue | pass (user report) | pass (user report) | pass (user report) | pass (user report) | pass (user report) |
| Corrected before Continue | pass (user report) | pass (user report) | pass (user report) | pass (user report) | pass (user report) |

Each route must restore the exact attempt/item and the inline hidden/revealed/accepted state. A reopened tab is not a browser-process restart. For Docker restart, tell the assistant which state is ready; it can restart api/web without deleting the volume.

5. Try again after saved reveal and reload: no old response/result returns. Submit a new miss: it remains hidden until its own Show answer. Continue into a retry copy: old feedback/reveal does not transfer.
6. Confirm existing automatic uncorrected rounds, correction exclusion, opening score, Continue, Start Over and Exit; repeated reveal creates no new attempt or recall credit. Exit keeps attempts and starts no extra round.
7. Public reads retain original explanations/chunks/alternatives; detailed teaching is intentionally absent from this Phase 1 focus UI, not erased from saved data.

The user reported no issues or unavailable routes. Existing deferred education and multi-blank/drag-and-drop follow-ups remain deferred; this approval does not implement them.

**Handoff:** approved T3 is recorded in 01-18-SUMMARY.md and 01-VALIDATION.md. The separate phase-close learner smoke and re-verification remain pending. Original EVAL-05 remains partial/deferred and Phase 1 open. At checkpoint recording no Git mutations had been performed. Subsequent user Да explicitly authorizes scoped commit/push to the current branch; Git history/handoff records that result, not original EVAL-05 or phase closure.
