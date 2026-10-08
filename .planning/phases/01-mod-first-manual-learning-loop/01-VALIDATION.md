---
phase: "01"
slug: "mod-first-manual-learning-loop"
status: validated
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-28"
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution. Seeded from `01-RESEARCH.md` ## Validation Architecture. Task rows mapped to plans written 2026-09-29.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x (backend); Vitest 5.0.x (frontend) |
| **Config file** | none — Wave 0 / plan 01-01 installs `pyproject.toml` and Vitest config |
| **Quick run command** | Task `<automated>` command only. Do not use Compose or the OpenAPI diff as the quick command. |
| **Full suite command** | Wave 8 only: `uv run pytest -q` and `npx --prefix frontend vitest run` and `docker compose up -d --wait` and the OpenAPI client diff |
| **Estimated runtime** | unknown until Wave 0; target under 120 seconds |

---

## Sampling Rate

Progressive gates. Do not run a later wave's command before the plan that creates it.

- **After every task commit:** Run that task's `<automated>` command only.
- **Wave 1 (01-01):** `uv run pytest -q` for the tests that exist. No Compose. No OpenAPI diff. No frontend Vitest.
- **Wave 2 and later, only after 01-10 is green:** `docker compose up -d --wait` is a legal gate. Do not run Compose before 01-10.
- **Wave 5 and later, only after 01-06 is green:** `npx --prefix frontend vitest run` for frontend tasks. Do not require Vitest before the frontend test files exist.
- **OpenAPI gate only after 01-08 (wave 7):** `uv run python -m lait.adapters.http.export_openapi`, then `npm --prefix frontend run openapi:generate`, then `git diff --exit-code -- frontend/src/api/generated`. Do not run this gate on waves 1–6.
- **Final wave (wave 8, plan 01-09):** full suite — `uv run pytest -q`, `npx --prefix frontend vitest run`, `docker compose up -d --wait`, and the OpenAPI dirty-diff.
- **Before `/gsd-verify-work`:** the wave 8 full suite must be green.
- **Max feedback latency:** 120 seconds. Compose is a wave gate, not the per-task check.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-T2 | 01-01 | 1 | LESS-01 | T-01-01 | Paste creates a lesson with no account | unit | `uv run pytest backend/tests/application/test_lesson_create.py -q` | ❌ W0 | ⬜ pending |
| 01-01-T2 | 01-01 | 1 | LESS-02 | T-01-01 | List and open lessons | unit | `uv run pytest backend/tests/application/test_lesson_list.py -q` | ❌ W0 | ⬜ pending |
| 01-01-T2 | 01-01 | 1 | MODL-12 | T-01-01 | Handlers do not call repositories from HTTP routers | unit | `uv run pytest backend/tests/application/test_lesson_create.py -q` | ❌ W0 | ⬜ pending |
| 01-10-T2 | 01-10 | 2 | PLAT-03 | T-01-24 | Compose is healthy only after migrations | smoke | `docker compose up -d --wait` | ❌ W0 | ⬜ pending |
| 01-02-T2 | 01-02 | 2 | MODL-01 | T-01-04 | Invalid manifest prevents startup | unit | `uv run pytest backend/tests/catalog/test_startup_validation.py -q` | ❌ W0 | ⬜ pending |
| 01-02-T2 | 01-02 | 2 | MODL-02 | T-01-05 | `describe()` returns public fields; live rows are `active` | unit | `uv run pytest backend/tests/catalog/test_describe.py -q` | ❌ W0 | ⬜ pending |
| 01-02-T2 | 01-02 | 2 | MODL-03 | T-01-06 | Proof catalog entry registers; learner list hides it | unit | `uv run pytest backend/tests/catalog/test_list_visible_for.py -q` | ❌ W0 | ⬜ pending |
| 01-03-T1 | 01-03 | 2 | ANLY-08 | T-01-07 | Exact span; overlap rejected; touching edges allowed | unit | `uv run pytest backend/tests/domain/test_spans.py backend/tests/application/test_learning_unit_add.py -q` | ❌ W0 | ⬜ pending |
| 01-03-T2 | 01-03 | 2 | ANLY-08 | T-01-08 | Logical-removed span does not block re-add; new id | unit | `uv run pytest backend/tests/application/test_learning_unit_remove.py::test_logical_removed_span_can_be_readded_as_new_unit -q` | ❌ W0 | ⬜ pending |
| 01-04-T1 | 01-04 | 3 | EXER-03 | T-01-09 | Gap Fill via registry; one unit skips drag (module) | unit | `uv run pytest backend/tests/modules/exercise_gap_fill/test_generate.py -q` | ❌ W0 | ⬜ pending |
| 01-04-T1 | 01-04 | 3 | EVAL-01 | T-01-09 | Drag checks unit id; typed match is trim and casefold | unit | `uv run pytest backend/tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ W0 | ⬜ pending |
| 01-04-T1 | 01-04 | 3 | EVAL-04 | T-01-10 | Only `correct` and `incorrect` | unit | `uv run pytest backend/tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ W0 | ⬜ pending |
| 01-04-T1 | 01-04 | 3 | EVAL-05 | T-01-11 | Template explanation; nullable natural alternative; used/missed | unit | `uv run pytest backend/tests/modules/exercise_gap_fill/test_feedback.py -q` | ❌ W0 | ⬜ pending |
| 01-05-T1 | 01-05 | 4 | EXER-01 | T-01-12 | Generate only from accepted units; status stored | unit | `uv run pytest backend/tests/application/test_exercise_generate.py -q` | ❌ W0 | ⬜ pending |
| 01-05-T1 | 01-05 | 4 | EXER-02 | T-01-13 | One item; unit set freezes | unit | `uv run pytest backend/tests/application/test_practice_start.py -q` | ❌ W0 | ⬜ pending |
| 01-05-T1 | 01-05 | 4 | EXER-07 | T-01-12 | Submit, feedback, next item, session stays open | unit | `uv run pytest backend/tests/application/test_submit_attempt.py -q` | ❌ W0 | ⬜ pending |
| 01-11-T1 | 01-11 | 5 | EXER-07 | T-01-14 | practice.start_over keeps Attempts; HTTP only maps DTOs | unit | `uv run pytest backend/tests/application/test_practice_finish_and_start_over.py -q` | ❌ W0 | ⬜ pending |
| 01-06-T1 | 01-06 | 5 | LESS-01 | T-01-15 | Create Lesson UI + empty/loading copy | component | `npx --prefix frontend vitest run src/features/lesson/LessonWorkspacePage.test.tsx` | ❌ W0 | ⬜ pending |
| 01-06-T3 | 01-06 | 5 | LESS-02 | T-01-15 | Lesson List UI states | component | `npx --prefix frontend vitest run src/features/lesson/LessonListPage.test.tsx` | ❌ W0 | ⬜ pending |
| 01-06-T2 | 01-06 | 5 | ANLY-08 | T-01-15 | Unit capture UI; overlap copy; emoji UTF-16 offsets become code points | component | `npx --prefix frontend vitest run src/features/lesson/LearningUnitsStage.test.tsx --reporter=verbose` | ❌ W0 | ⬜ pending |
| 01-06-T1 | 01-06 | 5 | EXER-01 | T-01-16 | Generating… then terminal status UI | component | `npx --prefix frontend vitest run src/features/lesson/LessonWorkspacePage.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T1 | 01-07 | 6 | EXER-02 | T-01-17 | Focus Practice Mode one item | component | `npx --prefix frontend vitest run src/features/lesson/FocusPracticeMode.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T1 | 01-07 | 6 | EXER-03 | T-01-17 | Gap Fill renderer via registry | component | `npx --prefix frontend vitest run src/registries/renderers/gapFillRenderer.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T1 | 01-07 | 6 | EXER-07 | T-01-17 | Submit, feedback, Continue in session | component | `npx --prefix frontend vitest run src/features/lesson/FocusPracticeMode.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T1 | 01-07 | 6 | EVAL-01 | T-01-17 | Chip submits unit id; typed field submits text | component | `npx --prefix frontend vitest run src/registries/renderers/gapFillRenderer.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T1 | 01-07 | 6 | EVAL-04 | T-01-17 | UI shows correct\|incorrect only | component | `npx --prefix frontend vitest run src/features/lesson/FocusPracticeMode.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T2 | 01-07 | 6 | EVAL-05 | T-01-19 | Feedback card fields; omit null alternative | component | `npx --prefix frontend vitest run src/features/lesson/FeedbackStage.test.tsx` | ❌ W0 | ⬜ pending |
| 01-07-T3 | 01-07 | 6 | D-20 | T-01-18 | Proof renderer mounts only in maintainer/test path | component | `npx --prefix frontend vitest run src/registries/renderers/proofRenderer.test.ts` | ❌ W0 | ⬜ pending |
| 01-08-T2 | 01-08 | 7 | PLAT-09 | T-01-20 | Generated client matches OpenAPI | contract | `uv run python -m lait.adapters.http.export_openapi` then `npm --prefix frontend run openapi:generate` then `git diff --exit-code -- frontend/src/api/generated` | ❌ W0 | ⬜ pending |
| 01-08-T2 | 01-08 | 7 | MODL-12 | T-01-21 | HTTP remains DTO adapter over handlers | contract | same OpenAPI export path | ❌ W0 | ⬜ pending |
| 01-09-T1 | 01-09 | 8 | MODL-03 | T-01-22 | Removing proof catalog entry leaves Core and Gap Fill working | unit | `uv run pytest backend/tests/catalog/test_proof_removal.py -q` | ❌ W0 | ⬜ pending |
| 01-09-T2 | 01-09 | 8 | PLAT-10 | T-01-23 | Core, persistence, and modules test separately | unit | `uv run pytest backend/tests/domain backend/tests/adapters/persistence backend/tests/modules -q` | ❌ W0 | ⬜ pending |
| 01-09-T2 | 01-09 | 8 | MODL-12 | T-01-23 | Handlers do not import HTTP or tables | unit | `uv run pytest backend/tests/application/test_handler_isolation.py -q` | ❌ W0 | ⬜ pending |
| 01-09-T3 | 01-09 | 8 | PLAT-03 | T-01-24 | Full-phase Compose health | smoke | `docker compose up -d --wait` | ❌ W0 | ⬜ pending |
| 01-09-T3 | 01-09 | 8 | PLAT-03 | T-01-01 | Full-phase pytest gate | unit | `uv run pytest -q` | ❌ W0 | ⬜ pending |
| 01-17-T1 | 01-17 | 12 | EVAL-05 | T-01-46, T-01-47 | Real reopened SQLite → query → HTTP preserves nonempty chunks, non-null alternative, original explanation and identity | integration | `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests/adapters/http/test_http_dto_mapping.py -q` | Existing file; assertions implemented | ✅ green — 5 passed (01-17 tracer rerun included) |
| 01-17-T2 | 01-17 | 12 | EVAL-05 | T-01-46, T-01-47 | Independent saved-payload projections, genuine empty/null and unchanged retry/finish/score | repository/application | `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests/adapters/persistence/test_lesson_reopen_reads.py backend/tests/application/test_lesson_reopen_reads.py backend/tests/application/test_practice_retry.py backend/tests/application/test_practice_finish_and_start_over.py -q` | Existing files; assertions implemented | ✅ green — 28 passed |
| 01-17-T2 | 01-17 | 12 | EVAL-05 | T-01-47 | Regenerated feedback DTO is consumed by the existing generated alias; PLAT-09 stays closed | type/contract | `npm --prefix frontend run typecheck` | Existing script; DTO regenerated | ✅ green — generated required-field assertion and typecheck passed |
| 01-18-T1 | 01-18 R2 | 13 | EVAL-05 partial, EVAL-01 | T-01-48, T-01-50 | Inline accepted reference in green; incorrect submitted/revealed reference; no Details/education/duplicate input/card; cleared Try again before/after reveal; inert answer text | component | `node frontend/node_modules/vitest/vitest.mjs run --root frontend src/registries/renderers/gapFillRenderer.test.tsx --maxWorkers=1` | Existing, revised per D-32–D-37 | ✅ green — 16 passed, tracer rerun 16 passed |
| 01-18-T2 | 01-18 R2 | 13 | EVAL-05 partial, EXER-07 | T-01-49 | Exact pending/final-success restore, rich real payload at renderer seam, retry-copy/stale-response isolation; saved Try again clears without commands or stale reveal | component | `node frontend/node_modules/vitest/vitest.mjs run --root frontend src/features/lesson/LessonWorkspacePage.test.tsx src/features/lesson/FocusPracticeMode.test.tsx src/features/lesson/stages/FeedbackStage.test.tsx --maxWorkers=1` | Existing, revised assertions; production restore retained | ✅ green — 69 passed |
| 01-18-T2 | 01-18 R2 | 13 | EVAL-05 partial, EXER-07 | T-01-49 | Frozen retry/score/Continue/Start Over/Exit and saved rich-payload regressions; no LLM/new template or domain change | full regression/type/build | `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests -q`; `node frontend/node_modules/vitest/vitest.mjs run --root frontend --maxWorkers=1`; `npm --prefix frontend run typecheck`; `npm --prefix frontend run build` | Existing | ✅ green — backend 129, frontend 105; typecheck/build passed |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Task ID legend: `{plan}-T{taskIndex}` matching task order inside each PLAN.md (checkpoints count in the index).*

---

## Wave 0 Requirements

- [ ] `backend/tests/` layout — application, domain, catalog, modules, persistence
- [ ] Frontend Vitest config and renderer registry test
- [ ] `docker-compose.yml` healthcheck that becomes ready only after Alembic
- [ ] `lait.adapters.http.export_openapi` plus `npm run openapi:generate`
- [ ] CI step that runs pytest, vitest, compose health, and `git diff --exit-code -- frontend/src/api/generated`

---

## Manual-Only Verifications

Already-executed Phase 1 plans are not rewritten to insert checkpoints. The rule in `docs/governance/MANUAL_UI_VERIFICATION.md` still gates phase close, and it applies to every later plan.

Follow-up `01-13-PLAN.md` (not executed): automated reads are `uv run pytest backend/tests/application/test_lesson_reopen_reads.py backend/tests/adapters/persistence/test_lesson_reopen_reads.py backend/tests/application/test_handler_isolation.py -q` and `npx --prefix frontend vitest run src/features/lesson/LessonWorkspacePage.test.tsx src/features/lesson/stages/FeedbackStage.test.tsx`. The blocking-human Docker check is the last task of that plan. Those commands do not replace it.

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Viewport wrap/truncate backstops from UI-SPEC | UI-SPEC long-text rows | `verification: backstop` — abstain without human/viewport evidence | Spot-check Lesson List title truncate, create-title wrap, Gap Fill wrap at 320px after plan 01-07 |
| Phase-close learner-flow smoke | LESS-01, LESS-02, ANLY-08, EXER-01, EXER-02, EXER-07, EVAL-01, EVAL-04, EVAL-05 | Vitest and pytest do not show Compose reopen | On `http://127.0.0.1:5173`, paste a lesson, add and accept a unit, finish one Gap Fill item, reload, open the same lesson from `/`, then `docker compose restart` without deleting the volume and open it again. Source and units must still be there. |
| 01-18-T3 R2 inline-result checkpoint — APPROVED 2026-10-07, user report, no observations | Narrowed Phase 1 EVAL-05, EXER-07, EVAL-01; D-32–D-37 | Required blocking-human Docker approval; R1 remains not approved | User: “ручная проверка пройдена без замечаний approved.” Published R2 checklist approved as a whole: inline results/retry/disclosure and four states × reload/direct URL/list return/full browser-process restart/Docker restart with volume kept. Recorded as user-reported passes, not assistant-observed clicks; no per-route screenshots/logs supplied. Exact payload remains saved. Full teaching/chunk display explicitly deferred, not passed. See `01-18-CHECKPOINT.md` and `01-18-SUMMARY.md`. |
| Final phase manual learner-flow smoke — PASS 2026-10-08, user report; separate from 01-18 R2 approval | Narrowed Phase 01 success criteria 1–3; original EVAL-05 partial/deferred | Whole-phase Docker smoke required before phase.complete; user-observed UI evidence | `01-UAT.md` tests 1–14 explicitly passed: retained-volume Docker restart; paste → capture/accept → generate → wrong response/reveal/retry/self-correction → inline accepted result → Continue/Exit with score/history and unit unfreeze. Test 12 confirms four feedback states across reload, direct URL, list return, actual browser-process and Docker/app restarts with volume kept; tests 13–14 cover 320px and workspace/Feedback. User reports only, no assistant-observed clicks or route screenshots. Real saved payload uses the existing automated checks, not a new manual inspection. Detailed teaching/chunk/alternative UI stays deferred. Canonical re-verification still required before phase completion. |

---

## Current R2 Execution Evidence — 2026-10-07

Latest acceptance D-32–D-37 intentionally narrows Phase 1: detailed teaching/chunk/alternative presentation is deferred; original full EVAL-05 is partial, not complete. First checkpoint was explicitly not approved; historical R1 results are below and do not approve R2.

- Current automatic checks: renderer RED 10 failed/6 passed before inline implementation, GREEN/tracer rerun 16/16; restore/Focus/stage target 69 passed; full backend 129 and full frontend 105 passed; typecheck/build passed. Complete saved payload remains asserted at the renderer seam with exact original explanation/nonempty chunks/non-null alternative. Backend and restore production unchanged in R2.
- Plan frontmatter/structure valid, D-32–D-37 decision coverage 6/6; current six failure directions valid; UI safety gate has no block. Inline review is not claimed as independent-agent review; three historical missing failure directions in executed 01-15/16 are recorded in 01-18-PLAN-CHECK.md, not reopened here.
- Docker rebuilt and api/web restarted with volume kept; API ok, web HTTP 200 serving `index-I9J8SvOc.js` / `index-D6b_DoN8.css`. This run's baseline and post-restart reads contain identical 1 lesson / 188 attempts, including 152 nonempty used and 36 nonempty missed arrays; SHA256 `E6E8B582FB72B561867F3E3C6844E75D40AA3CD7BDE58DFB93130205D5F70B6B`. R1's 181 is historical, not reused as the new baseline. No user-data writes/deletion by the assistant.
- R2 human four-state × five-route checklist approved by user report on 2026-10-07 without observations. No individual route logs/screenshots supplied; approval is not claimed as assistant-observed evidence. Non-null-alternative **display** remains explicitly deferred; its payload preservation stays automatically checked. Detailed approval: `01-18-CHECKPOINT.md`; old record: `01-18-CHECKPOINT-R1.md` (not approved).
- 01-18 SUMMARY records all three tasks complete. No source edits or test rerun in this approval-recording turn, no commits/push or Phase 1 completion. Separate phase-close smoke and re-verification stay pending; PLAT-09 stays closed.

## Validation Audit — 2026-10-08 UAT completion

`gsd-validate-phase` post-UAT audit reused the existing requirement/task map and recorded implementation regression evidence. The current coverage classifier accepted all 18 SUMMARY blocks with zero parsing errors: 62 auto-passed entries and 11 human-judgment entries. Those human entries plus the startup/source-to-practice checks map to the 14 manual tests in `01-UAT.md`, now explicitly passed by the user.

No uncovered behavior was identified within approved narrowed Phase 1 D-32–D-37 acceptance. Existing 01-17/18 tests cover rich/empty/malformed saved feedback, exact identity, disclosure, stale response isolation, clearing retry and frozen progression. No new tests or implementation edits were needed. Previously recorded backend 129/frontend 105/typecheck/build results are reused, not newly executed here.

| Metric | Count / scope |
| --- | --- |
| SUMMARY coverage blocks classified | 18; zero errors |
| Recorded automated UAT entries | 62 passed |
| Human Docker learner-flow checks | 14 passed by user report |
| Current-session issues/pending/blocked/skipped | 0 / 0 / 0 / 0 |
| New required validation gaps under D-32–D-37 | 0 |
| Original requirement still partial/deferred | EVAL-05 teaching/chunk/alternative presentation → Phase 5 |

`nyquist_compliant: true` remains scoped to the approved Phase 1 acceptance; it does not claim delivery of original full EVAL-05. Historical Wave 0/per-task placeholder rows and dated audits above retain their original evidence; this audit and the completed UAT are the current completion record. Canonical verification must still be regenerated before phase transition.

## Historical R1 Gap Execution Evidence — 2026-10-07 (superseded presentation, not approved)

01-17 automatic tasks are complete. 01-18 T1/T2 were implemented inline after the user selected option 3; T3 is the sole final blocking-human Docker gate and remains pending. Detailed commands, TDD results, restoration matrix and resume instructions: `01-18-CHECKPOINT.md`. This does not supersede historical audit evidence or sign off the phase.

- Full current backend: 129 passed; full current frontend: 104 passed (9 files). Build and typecheck passed. Renderer/workspace targeted: 74 passed; module feedback/evaluate: 6 passed; FocusPracticeMode/FeedbackStage: 10 passed; backend retry/finish: 6 passed.
- Current answer-free module test name is `test_correct_explanation_is_answer_free_and_records_used`; the older D-18 test name in the historical audit below describes that audit's baseline, not the current acceptance contract.
- Docker serving images rebuilt, both healthy; production web HTTP 200 at `http://127.0.0.1:5173`, matching `index-BTGVBf0C.js`. Actual api/web restart retained the named volume. Read-only public queries returned identical full payloads for 1 lesson / 181 attempts before/after restart and after final rebuild (146 nonempty used, 35 nonempty missed arrays), SHA256 `4A9ED479A045AC6250051ECCDFF58BD66B6A2B50E1E888D675AE643B1F267FDD`.
- Automatic Docker payload preservation is not human UI approval. All four card states × five re-entry/restart routes remain pending manual evidence, including genuine browser-process restart and final success before Continue. Live non-null-alternative fixture is unavailable (0), so its manual check remains pending; rich non-null automatic fixtures passed.
- No volume deletion, learner-data writes, staging, commits or pushes. EVAL-05, Phase 1, manual sign-off and separate phase-close learner smoke remain open. PLAT-09 is not reopened.

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

---

## Validation Audit — 2026-10-06

Nyquist stays false. Sixteen requirements have a passing behavioral test. PLAT-09 fails: live OpenAPI exposes `practice.advance`, and `frontend/src/api/generated/sdk.gen.ts` does not. `lessonApi.advancePractice` posts through the raw client instead of a generated function. Implementation was not patched.

`docker compose up -d --wait` was not executed in this audit. PLAT-03 is filled by the entrypoint and Compose-contract test below.

Known behavior left untouched: same-session uncorrected rounds, opening-size score, `test_named_target_on_a_repeat_copy_advances_once`, Answer `autocomplete="off"`.

| Requirement | Test | Result |
|-------------|------|--------|
| LESS-01 | `backend/tests/application/test_lesson_create.py::test_lesson_create_persists_exact_utf8_source`; `backend/tests/adapters/http/test_http_dto_mapping.py::test_http_maps_create_dto_and_rejects_empty_source`; `frontend/src/features/lesson/LessonListPage.test.tsx` | FILLED |
| LESS-02 | `backend/tests/application/test_lesson_list.py::test_lesson_list_and_get_round_trip`; `frontend/src/features/lesson/LessonListPage.test.tsx`; `frontend/src/features/lesson/LessonWorkspacePage.test.tsx` | FILLED |
| ANLY-08 | `backend/tests/application/test_learning_unit_add.py::test_add_stores_exact_span_text_as_draft`; `frontend/src/features/lesson/LearningUnitsStage.test.tsx` | FILLED |
| EXER-01 | `backend/tests/application/test_exercise_generate.py::test_generate_skips_drafts_and_persists_only_terminal_status`; `frontend/src/features/lesson/LessonWorkspacePage.test.tsx` | FILLED |
| EXER-02 | `backend/tests/application/test_practice_start.py::test_practice_get_returns_one_current_typed_item_for_one_unit`; `frontend/src/features/lesson/FocusPracticeMode.test.tsx` | FILLED |
| EXER-03 | `backend/tests/catalog/test_list_visible_for.py::test_learner_list_includes_gap_fill_and_omits_proof`; `backend/tests/modules/exercise_gap_fill/test_generate.py::test_one_accepted_unit_blanks_only_the_target_span`; `frontend/src/registries/renderers/gapFillRenderer.test.tsx` | FILLED |
| EXER-07 | `backend/tests/application/test_submit_attempt.py::test_submit_stores_attempt_feedback_and_advances_while_session_stays_open`; `frontend/src/features/lesson/FocusPracticeMode.test.tsx` | FILLED |
| EVAL-01 | `backend/tests/modules/exercise_gap_fill/test_evaluate.py::test_drag_is_correct_when_submitted_learning_unit_id_matches`; `test_typed_match_strips_ends_and_ignores_case_only` | FILLED |
| EVAL-04 | `backend/tests/modules/exercise_gap_fill/test_evaluate.py::test_gap_fill_emits_only_correct_or_incorrect`; `frontend/src/features/lesson/FocusPracticeMode.test.tsx` | FILLED |
| EVAL-05 | `backend/tests/modules/exercise_gap_fill/test_feedback.py::test_correct_explanation_matches_d18_and_records_used`; `frontend/src/features/lesson/FeedbackStage.test.tsx`; `frontend/src/features/lesson/FocusPracticeMode.test.tsx` | FILLED |
| MODL-01 | `backend/tests/catalog/test_startup_validation.py::test_api_incompatible_manifest_refuses_startup` (also duplicate id, unresolved dependency, empty catalog) | FILLED |
| MODL-02 | `backend/tests/catalog/test_describe.py::test_describe_returns_public_active_rows` | FILLED |
| MODL-03 | `backend/tests/modules/exercise_proof/test_contract.py::test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill`; `backend/tests/catalog/test_proof_removal.py::test_proof_removal`; `frontend/src/registries/renderers/proofRenderer.test.ts` | FILLED |
| MODL-12 | `backend/tests/application/test_handler_isolation.py::test_handler_isolation`; `backend/tests/application/test_lesson_list.py::test_http_routers_delegate_to_handlers_not_repositories` | FILLED |
| PLAT-03 | `backend/tests/adapters/persistence/test_compose_migrate_then_health.py` | FILLED |
| PLAT-09 | `backend/tests/adapters/http/test_openapi_client_drift.py::test_typescript_client_matches_openapi_and_ci_rejects_drift` | FILLED |
| PLAT-10 | `backend/tests/application/test_handler_isolation.py::test_handler_isolation` | FILLED |

### PLAT-09 closure

The 2026-10-06 escalation failed because `sdk.gen.ts` had no `practiceAdvance`. Closed the same day by `uv run python -m lait.adapters.http.export_openapi` and `npm --prefix frontend run openapi:generate`. Generated files were not hand-edited. A second export+generate left the same SHA256 for `openapi.json` and the four generated files. `advancePractice` now calls `practiceAdvance`. `pytest backend/tests/adapters/http/test_openapi_client_drift.py -q` passed. `npm run typecheck` passed. Vitest `FocusPracticeMode.test.tsx` and `LessonWorkspacePage.test.tsx` passed, 38 tests.

### Commands run

- `uv run pytest` on the backend files in the map above, including `test_compose_migrate_then_health.py`: 80 passed.
- `uv run pytest backend/tests/adapters/http/test_openapi_client_drift.py -q`: 1 failed.
- `npx --prefix frontend vitest run` on the frontend files in the map, `--maxWorkers=1`: 8 files, 65 passed.
