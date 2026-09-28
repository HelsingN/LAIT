---
phase: "01"
slug: "mod-first-manual-learning-loop"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-28"
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution. Seeded from `01-RESEARCH.md` ## Validation Architecture. Task rows stay pending until plans exist.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x (backend); Vitest 5.0.x (frontend) |
| **Config file** | none — Wave 0 installs `pyproject.toml` and Vitest config |
| **Quick run command** | `uv run pytest -q` and `npx vitest run` |
| **Full suite command** | `uv run pytest` and `npx vitest run` and `docker compose up -d --wait` and the OpenAPI client diff |
| **Estimated runtime** | unknown until Wave 0; target under 120 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest -q` and `npx vitest run`
- **After every plan wave:** Run `uv run pytest` and `npx vitest run` and `docker compose up -d --wait` and `git diff --exit-code -- frontend/src/api/generated` after `uv run python -m lait.adapters.http.export_openapi` and `npm run openapi:generate`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| — | — | 0 | LESS-01 | — | Paste creates a lesson with no account | unit | `uv run pytest tests/application/test_lesson_create.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | LESS-02 | — | List and open lessons | unit | `uv run pytest tests/application/test_lesson_list.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | ANLY-08 | — | Exact span; overlap rejected; touching edges allowed | unit | `uv run pytest tests/domain/test_spans.py tests/application/test_learning_unit_add.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EXER-01 | — | Generate only from accepted units; status stored | unit | `uv run pytest tests/application/test_exercise_generate.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EXER-02 | — | One item; unit set freezes | unit | `uv run pytest tests/application/test_practice_start.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EXER-03 | — | Gap Fill via registry; one unit skips drag | unit | `uv run pytest tests/modules/exercise_gap_fill/test_generate.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EXER-07 | — | Submit, feedback, next item, session stays open | unit | `uv run pytest tests/application/test_submit_attempt.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EVAL-01 | — | Drag checks unit id; typed match is trim and casefold | unit | `uv run pytest tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EVAL-04 | — | Only `correct` and `incorrect` | unit | `uv run pytest tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | EVAL-05 | — | Template explanation; nullable natural alternative; used/missed | unit | `uv run pytest tests/modules/exercise_gap_fill/test_feedback.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | MODL-01 | — | Invalid manifest prevents startup | unit | `uv run pytest tests/catalog/test_startup_validation.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | MODL-02 | — | `describe()` returns public fields; live rows are `active` | unit | `uv run pytest tests/catalog/test_describe.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | MODL-03 | — | Removing the proof catalog entry leaves Core and Gap Fill working | unit | `uv run pytest tests/catalog/test_proof_removal.py -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | MODL-12 | — | Handlers do not import HTTP or tables | unit | `uv run pytest tests/application -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | PLAT-03 | — | Compose is healthy only after migrations | smoke | `docker compose up -d --wait` | ❌ W0 | ⬜ pending |
| — | — | 0 | PLAT-09 | — | Generated client matches OpenAPI | contract | `uv run python -m lait.adapters.http.export_openapi` then `npm run openapi:generate` then `git diff --exit-code -- frontend/src/api/generated` | ❌ W0 | ⬜ pending |
| — | — | 0 | PLAT-10 | — | Core, persistence, and modules test separately | unit | `uv run pytest tests/domain tests/adapters/persistence tests/modules -q` | ❌ W0 | ⬜ pending |
| — | — | 0 | D-20 | — | Proof renderer mounts only in the maintainer/test path | component | `npx vitest run src/registries/renderers/proofRenderer.test.ts` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/` layout — application, domain, catalog, modules, persistence
- [ ] Frontend Vitest config and renderer registry test
- [ ] `compose.yaml` healthcheck that becomes ready only after Alembic
- [ ] `lait.adapters.http.export_openapi` plus `npm run openapi:generate`
- [ ] CI step that runs pytest, vitest, compose health, and `git diff --exit-code -- frontend/src/api/generated`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| None for the Phase 1 contract | — | Browser projects are PLAT-11, later | All phase behaviors above have automated verification |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
