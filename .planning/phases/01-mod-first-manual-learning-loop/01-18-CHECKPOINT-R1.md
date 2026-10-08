---
phase: 01-mod-first-manual-learning-loop
plan: 18
status: superseded-not-approved
checkpoint_task: 3
gate: blocking-human
completed_automatic_tasks: [1, 2]
human_approval: not-approved
commits: 0
---

# 01-18 — first checkpoint (superseded, not approved)

The user explicitly reported observations, not approved, and authorized D-32–D-37 narrowing. This historical record is retained as evidence only; its Details/educational-content acceptance and checklist are no longer current. Use 01-18-CHECKPOINT.md revision 2.

Execution handoff, 2026-10-07. The user selected option **3: execute inline** after the executor stopped before its first write. The root guard passed before inline edits. T1/T2 are implemented and automatically verified. This is not a SUMMARY, human approval, EVAL-05 closure or Phase 1 completion.

## What is ready

- Compact Feedback shows the raw submitted answer once. Details starts collapsed and supports keyboard operation; it resets for a new result on the same item.
- Incorrect results mount only an answer-free explanation until parameterless Show answer or a correct/corrected result. Opening Details alone mounts no hidden expected/chunks/alternative/original solution-bearing prose.
- After disclosure, actual explanation, used/missed chunk associations and nullable alternative are available. Positively identified labeled/quoted answer echoes link to the existing answer instead of repeating it. Ordinary prose, short-word substrings, overlapping distinct chunks, raw whitespace and inert markup remain intact. Legacy compatibility does not rewrite saved records.
- Saved feedback is read from the exact saved attempt, with its real chunks and alternative. Versioned presentation records store item/attempt identity and prompt context only, not replacement education. Correct/corrected cards—including a final success—survive restoration before Continue without rewinding the server cursor. Missing/corrupt history is an error with read retry, never synthetic empty feedback or implicit finish.
- Exact item/copy/attempt bindings, request-generation guards and retained-callback guards prevent old reveals and late hydration/submit/Continue results from attaching to new cards. Legacy boolean reveal flags fail closed. Details/Show answer make no domain command.
- Retry rounds, independent-recall grading, opening score, Continue, Start Over and Exit are unchanged. PLAT-09 stays closed; no dependency or database-schema change.

Owned 01-18 production files: module `feedback.py`, `GapFillRenderer.tsx`/CSS, renderer `types.ts`, `stageState.ts`, `LessonWorkspacePage.tsx`. Test changes: module feedback, renderer, workspace; two necessary old-copy assertions in application submit and FocusPracticeMode were aligned with the approved answer-free/Details UX. Grading, cursor, score and Exit assertions were retained. Other pre-existing dirty files were preserved.

## Automatic evidence

All commands ran from `D:/Helsing/gitHub/LAIT`, without watch mode.

| Check | Actual result |
| --- | --- |
| Full backend: `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests -q` | 129 passed; no skipped tests; pre-existing Starlette/httpx deprecation warning only |
| Full frontend: `node frontend/node_modules/vitest/vitest.mjs run --root frontend --maxWorkers=1` | 104 passed, 9 files |
| Renderer + workspace targeted | 17 + 57 = 74 passed |
| T1 module feedback/evaluate targeted | 6 passed; grading tests unchanged |
| FocusPracticeMode + stages/FeedbackStage targeted | 10 passed; frozen interaction assertions retained |
| Backend retry + finish/start-over targeted | 6 passed |
| `npm --prefix frontend run typecheck` | Passed after final import placement |
| `npm --prefix frontend run build` | Passed; `index-BTGVBf0C.js`, `index-k0bpnhLT.css` |
| Ruff on the three 01-18 changed Python files | Passed |
| GSD UI safety gate | UI detected, UI-SPEC present, no block |
| `git diff --check`; staged diff; commits since execution baseline | Passed; staged diff empty; 0 commits, HEAD unchanged |

TDD: initial T1 renderer RED was 9 failed/6 passed and module RED 2 failed/4 passed for the old answer-echo templates. T1 GREEN was automatically rerun before T2. T2 RED demonstrated missing exact rich restore/final-success cards and fail-closed history recovery. Later added bare-label echo and late-unmounted-submit cases produced 2 failures, then passed after fixes. Final automatic totals above include additional snapshot/binding/late-Continue/new-result Details regressions. A Start Over test setup correction (missing confirmation click) is not counted as intentional RED evidence.

## Docker evidence — automatic, not human approval

`docker compose up -d --build --wait api web` succeeded; after the final import-only cleanup, `docker compose up -d --build --wait web` succeeded again. Both services are healthy. API `http://127.0.0.1:8000/health` returns `ok`; web `http://127.0.0.1:5173` returns HTTP 200 and serves the matching production bundle. No Vite dev server is used.

`docker compose restart api web` succeeded with the existing named volume retained. Read-only public lesson/attempt queries before and after restart, and after the final image rebuild, returned the same **1 lesson / 181 attempts**, including 146 nonempty used arrays and 35 nonempty missed arrays. Full sorted attempt payload JSON SHA256 stayed:

`4A9ED479A045AC6250051ECCDFF58BD66B6A2B50E1E888D675AE643B1F267FDD`

Digest reproduction: read `.lessons` from GET `/api/lessons`, collect each GET `/api/lessons/{id}/attempts` `.attempts`, sort by `attempt_id`, `ConvertTo-Json -InputObject $attempts -Depth 30 -Compress`, SHA256 over UTF-8 bytes. A final diagnostic initially treated the envelope as a flat list and got 404; the corrected envelope-aware read above returned the original digest. No data was created, edited, reseeded or deleted by these diagnostics.

The live volume has **0 non-null natural alternatives**. Real reopened SQLite and frontend fixtures cover rich non-null alternatives automatically. Manual non-null-alternative verification is **unavailable/pending**, not silently approved. Genuine null must have no empty alternative label.

## T3 — blocking human verification

Use **http://127.0.0.1:5173**, the same browser profile and this exact origin throughout. Images are current, volume kept. Fully quitting/relaunching the browser process is required; a new/reopened tab is not equivalent. Docker restart while a particular card is displayed is required; the automatic restart above does not approve its UI restoration.

1. Submit a wrong answer. Submitted appears once; Details starts closed. Keyboard-open it: meaningful safe mismatch explanation, no expected/solution-bearing education before Show answer.
2. For each row below, perform every route separately. Confirm the exact saved card and real educational data restore, hidden or disclosed as appropriate. For correct/corrected, do this **before Continue**; include a final success with exhausted server cursor. An identical submitted/reference value must not be repeated in Details.

| Card state | Reload | Direct `/lessons/{id}` | Lesson List return | Full browser-process restart | Docker/app restart, volume kept |
| --- | --- | --- | --- | --- | --- |
| Incorrect, undisclosed | pending | pending | pending | pending | pending |
| Same incorrect attempt after Show answer | pending | pending | pending | pending | pending |
| Correct, before Continue | pending | pending | pending | pending | pending |
| Corrected, before Continue | pending | pending | pending | pending | pending |

3. After Show answer, open Details: inspect actual expected value, original educational prose and used/missed phrase relationships; no repeated deliberate submitted/reference display. Check an existing legacy card where available. Record unavailable fixtures explicitly. Non-null alternative is currently unavailable; null omission is still checkable.
4. Try again/self-correct, then Continue into a repeat copy. No prior feedback/reveal transfers; a new miss remains hidden until its own Show answer. New results reset Details.
5. Toggle Details and Show answer repeatedly: no new attempt, cursor change, score change or recall credit. Check existing automatic still-uncorrected rounds, corrected exclusion, opening denominator, Continue, Start Over and Exit. Exit keeps attempts and starts no extra round.

For Docker/app restart, the assistant can run `docker compose restart api web` when the learner has the relevant card ready. Never delete the volume. Record each observation/route and any unavailable fixture, rather than substituting automatic tests for a manual pass.

**Resume signal:** reply `approved` after verification, or send observations. Classify observations as bug, UX debt, visual, workflow or deferred and propose the owning phase. An observation or “continue” is not approval. Do not start a dependent wave, create 01-18-SUMMARY, close EVAL-05 or Phase 1 before this gate is resolved. The separate phase-close Docker learner-flow smoke and parent re-verification remain pending after T3.

No staging, commit or push was performed or authorized. Resume from this checkpoint; do not rerun completed implementation as a new plan.
