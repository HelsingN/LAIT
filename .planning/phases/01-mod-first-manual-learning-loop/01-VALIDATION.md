---
phase: "01"
slug: "mod-first-manual-learning-loop"
status: draft
nyquist_compliant: false
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
| 01-06-T2 | 01-06 | 5 | ANLY-08 | T-01-15 | Unit capture UI; overlap copy | component | `npx --prefix frontend vitest run src/features/lesson/LearningUnitsStage.test.tsx` | ❌ W0 | ⬜ pending |
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

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Viewport wrap/truncate backstops from UI-SPEC | UI-SPEC long-text rows | `verification: backstop` — abstain without human/viewport evidence | Spot-check Lesson List title truncate, create-title wrap, Gap Fill wrap at 320px after plan 01-07 |
| None other for the Phase 1 contract | — | Browser projects are PLAT-11, later | Remaining phase behaviors above have automated verification |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
