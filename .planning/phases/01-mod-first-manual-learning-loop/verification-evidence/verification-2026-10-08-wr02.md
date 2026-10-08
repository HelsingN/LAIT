---
phase: 01-mod-first-manual-learning-loop
verified: 2026-10-08T01:58:44Z
status: gaps_found
score: 4/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
scope_revision: "01-18 R2; D-32–D-37"
scope_narrowing_approved: true
original_eval05_status: partial_deferred
uat_status: complete
uat_passed: 76
uat_human_passed: 14
uat_recorded_automated_passed: 62
phase_completion_performed: false
re_verification:
  previous_status: gaps_found
  previous_score: "3/5"
  previous_verified: "2026-10-06T20:52:32Z"
  gaps_closed:
    - "Saved educational payload loss on reopen: actual chunks/nullable alternative now survive all read projections and exact UI restoration."
    - "Phase-wide Docker learner smoke and restart/reopen evidence: user-reported UAT Tests 1–14 passed."
  gaps_remaining:
    - "WR-02: a delayed accepted submit can rewind the durable practice cursor."
  regressions: []
gaps:
  - gap_id: G-01-VER-20261008-WR02
    truth: "Learner can complete the exercise one item at a time without a delayed submit restoring an older cursor."
    status: failed
    reason: "Deterministic public-handler probe: a delayed incorrect submit writes its stale cursor after two other accepted submissions; persisted cursor changes from 2 to 0."
    artifacts:
      - path: backend/lait/adapters/persistence/repositories.py
        issue: "add_attempt writes stored.cursor = cursor from the earlier handler snapshot."
      - path: frontend/src/features/lesson/LessonWorkspacePage.tsx
        issue: "submit uses React pending state; Continue has no synchronous request lock. Epoch guards discard stale presentation responses but cannot undo server writes."
      - path: .planning/phases/01-mod-first-manual-learning-loop/verification-evidence/wr02_cursor_probe.py
        issue: "Fresh reproducible failing invariant; writes only a newly migrated temporary database."
    missing:
      - "Persistence must not restore an earlier cursor when accepting an attempt."
      - "A durable guard or serialization rule for overlapping submit/progression requests, with a passing regression reproduction."
deferred:
  - truth: "Original full EVAL-05 educational explanation, target-chunk analysis and optional natural-alternative presentation within the session."
    addressed_in: "Phase 5"
    evidence: "Approved 01-18-CONTEXT.md D-32–D-37, current ROADMAP success criterion 3 and REQUIREMENTS.md EVAL-05; reiterated by user in this verification request."
advisory:
  - finding: "O-01-9-visual: compact workspace Feedback requested."
    category: other
    reason: "UAT functional score/history checks passed. Request remains UX/visual debt; Phase 9 is only a proposed owner, not an approved deferral."
    evidence_status: "User functional pass plus concrete preference; no demonstrated failure of current narrowed acceptance."
human_verification: []
covered_files:
  - .github/workflows/ci.yml
  - .planning/phases/01-mod-first-manual-learning-loop/01-01-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-01-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-02-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-02-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-03-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-03-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-04-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-04-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-05-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-05-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-06-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-06-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-07-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-07-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-08-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-08-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-09-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-09-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-10-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-10-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-11-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-11-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-12-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-12-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-13-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-13-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-14-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-14-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-15-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-15-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-16-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-16-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-17-CONTEXT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-17-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-17-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-18-CHECKPOINT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-18-CONTEXT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-18-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-18-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-CONTEXT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-SECURITY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-UAT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-VALIDATION.md
  - .planning/phases/01-mod-first-manual-learning-loop/verification-evidence/wr02_cursor_probe.py
  - Dockerfile.api
  - Dockerfile.web
  - README.md
  - backend/alembic.ini
  - backend/alembic/env.py
  - backend/alembic/script.py.mako
  - backend/alembic/versions/20261001_0001_create_lessons.py
  - backend/alembic/versions/20261001_0002_create_learning_units.py
  - backend/alembic/versions/20261001_0003_create_practice_sessions.py
  - backend/alembic/versions/20261002_0004_one_open_practice_session.py
  - backend/lait/__init__.py
  - backend/lait/adapters/__init__.py
  - backend/lait/adapters/http/__init__.py
  - backend/lait/adapters/http/app.py
  - backend/lait/adapters/http/export_openapi.py
  - backend/lait/adapters/http/routers/__init__.py
  - backend/lait/adapters/http/routers/diagnostics.py
  - backend/lait/adapters/http/routers/exercises.py
  - backend/lait/adapters/http/routers/health.py
  - backend/lait/adapters/http/routers/learning_units.py
  - backend/lait/adapters/http/routers/lessons.py
  - backend/lait/adapters/http/routers/practice.py
  - backend/lait/adapters/persistence/__init__.py
  - backend/lait/adapters/persistence/database.py
  - backend/lait/adapters/persistence/lesson_repository.py
  - backend/lait/adapters/persistence/models.py
  - backend/lait/adapters/persistence/repositories.py
  - backend/lait/application/__init__.py
  - backend/lait/application/commands/__init__.py
  - backend/lait/application/commands/exercise_generate.py
  - backend/lait/application/commands/exercise_submit_attempt.py
  - backend/lait/application/commands/learning_unit_accept.py
  - backend/lait/application/commands/learning_unit_add.py
  - backend/lait/application/commands/learning_unit_remove.py
  - backend/lait/application/commands/lesson_create.py
  - backend/lait/application/commands/practice_advance.py
  - backend/lait/application/commands/practice_finish.py
  - backend/lait/application/commands/practice_start.py
  - backend/lait/application/commands/practice_start_over.py
  - backend/lait/application/commands/unit_set_freeze.py
  - backend/lait/application/ports.py
  - backend/lait/application/queries/__init__.py
  - backend/lait/application/queries/attempt_list_for_lesson.py
  - backend/lait/application/queries/chip_order.py
  - backend/lait/application/queries/exercise_latest_completed.py
  - backend/lait/application/queries/exercise_registry_list_visible.py
  - backend/lait/application/queries/learning_unit_list.py
  - backend/lait/application/queries/lesson_get.py
  - backend/lait/application/queries/lesson_list.py
  - backend/lait/application/queries/module_registry_describe.py
  - backend/lait/application/queries/practice_get.py
  - backend/lait/catalog/__init__.py
  - backend/lait/catalog/loader.py
  - backend/lait/catalog/manifests/module-manifest.schema.json
  - backend/lait/catalog/validation.py
  - backend/lait/domain/__init__.py
  - backend/lait/domain/exercise.py
  - backend/lait/domain/learning_unit.py
  - backend/lait/domain/lesson.py
  - backend/lait/domain/practice_session.py
  - backend/lait/domain/span.py
  - backend/lait/modules/__init__.py
  - backend/lait/modules/exercise_gap_fill/__init__.py
  - backend/lait/modules/exercise_gap_fill/contribution.py
  - backend/lait/modules/exercise_gap_fill/evaluate.py
  - backend/lait/modules/exercise_gap_fill/feedback.py
  - backend/lait/modules/exercise_gap_fill/generate.py
  - backend/lait/modules/exercise_gap_fill/manifest.json
  - backend/lait/modules/exercise_gap_fill/sentence_window.py
  - backend/lait/modules/exercise_proof/__init__.py
  - backend/lait/modules/exercise_proof/contribution.py
  - backend/lait/modules/exercise_proof/evaluate.py
  - backend/lait/modules/exercise_proof/generate.py
  - backend/lait/modules/exercise_proof/manifest.json
  - backend/tests/adapters/http/test_http_dto_mapping.py
  - backend/tests/adapters/http/test_openapi_client_drift.py
  - backend/tests/adapters/http/test_openapi_contract.py
  - backend/tests/adapters/persistence/test_compose_migrate_then_health.py
  - backend/tests/adapters/persistence/test_lesson_reopen_reads.py
  - backend/tests/adapters/persistence/test_lesson_repository.py
  - backend/tests/adapters/persistence/test_one_open_practice_session.py
  - backend/tests/application/test_exercise_generate.py
  - backend/tests/application/test_handler_isolation.py
  - backend/tests/application/test_learning_unit_accept.py
  - backend/tests/application/test_learning_unit_add.py
  - backend/tests/application/test_learning_unit_remove.py
  - backend/tests/application/test_lesson_create.py
  - backend/tests/application/test_lesson_list.py
  - backend/tests/application/test_lesson_reopen_reads.py
  - backend/tests/application/test_practice_chip_order.py
  - backend/tests/application/test_practice_finish_and_start_over.py
  - backend/tests/application/test_practice_retry.py
  - backend/tests/application/test_practice_start.py
  - backend/tests/application/test_submit_attempt.py
  - backend/tests/catalog/test_describe.py
  - backend/tests/catalog/test_list_visible_for.py
  - backend/tests/catalog/test_proof_removal.py
  - backend/tests/catalog/test_startup_validation.py
  - backend/tests/conftest.py
  - backend/tests/domain/test_spans.py
  - backend/tests/modules/exercise_gap_fill/test_evaluate.py
  - backend/tests/modules/exercise_gap_fill/test_feedback.py
  - backend/tests/modules/exercise_gap_fill/test_generate.py
  - backend/tests/modules/exercise_proof/test_contract.py
  - docker-compose.yml
  - docker/README.md
  - docker/api_entrypoint.py
  - docker/web-nginx.conf
  - frontend/openapi-ts.config.ts
  - frontend/openapi.json
  - frontend/package-lock.json
  - frontend/package.json
  - frontend/scripts/openapi-generate.mjs
  - frontend/src/api/client-config.ts
  - frontend/src/api/generated/client.gen.ts
  - frontend/src/api/generated/client/client.gen.ts
  - frontend/src/api/generated/client/index.ts
  - frontend/src/api/generated/client/types.gen.ts
  - frontend/src/api/generated/client/utils.gen.ts
  - frontend/src/api/generated/core/auth.gen.ts
  - frontend/src/api/generated/core/bodySerializer.gen.ts
  - frontend/src/api/generated/core/params.gen.ts
  - frontend/src/api/generated/core/pathSerializer.gen.ts
  - frontend/src/api/generated/core/queryKeySerializer.gen.ts
  - frontend/src/api/generated/core/serverSentEvents.gen.ts
  - frontend/src/api/generated/core/types.gen.ts
  - frontend/src/api/generated/core/utils.gen.ts
  - frontend/src/api/generated/index.ts
  - frontend/src/api/generated/sdk.gen.ts
  - frontend/src/api/generated/types.gen.ts
  - frontend/src/app/App.tsx
  - frontend/src/features/lesson/CreateLessonForm.tsx
  - frontend/src/features/lesson/FeedbackStage.test.tsx
  - frontend/src/features/lesson/FocusPracticeMode.module.css
  - frontend/src/features/lesson/FocusPracticeMode.test.tsx
  - frontend/src/features/lesson/FocusPracticeMode.tsx
  - frontend/src/features/lesson/LearningUnitsStage.test.tsx
  - frontend/src/features/lesson/LessonListPage.module.css
  - frontend/src/features/lesson/LessonListPage.test.tsx
  - frontend/src/features/lesson/LessonListPage.tsx
  - frontend/src/features/lesson/LessonWorkspacePage.module.css
  - frontend/src/features/lesson/LessonWorkspacePage.test.tsx
  - frontend/src/features/lesson/LessonWorkspacePage.tsx
  - frontend/src/features/lesson/api.ts
  - frontend/src/features/lesson/lessonApi.ts
  - frontend/src/features/lesson/selectionOffsets.ts
  - frontend/src/features/lesson/stageState.ts
  - frontend/src/features/lesson/stages/FeedbackStage.module.css
  - frontend/src/features/lesson/stages/FeedbackStage.test.tsx
  - frontend/src/features/lesson/stages/FeedbackStage.tsx
  - frontend/src/features/lesson/stages/GenerateExercisesStage.module.css
  - frontend/src/features/lesson/stages/GenerateExercisesStage.tsx
  - frontend/src/features/lesson/stages/LearningUnitsStage.module.css
  - frontend/src/features/lesson/stages/LearningUnitsStage.tsx
  - frontend/src/features/lesson/stages/PracticeStage.test.tsx
  - frontend/src/features/lesson/stages/PracticeStage.tsx
  - frontend/src/features/lesson/stages/SourceStage.module.css
  - frontend/src/features/lesson/stages/SourceStage.tsx
  - frontend/src/features/lesson/suggestTitle.ts
  - frontend/src/fonts/LICENSE-source-sans.md
  - frontend/src/fonts/LICENSE-source-serif.md
  - frontend/src/fonts/source-sans-3-400.woff2
  - frontend/src/fonts/source-sans-3-600.woff2
  - frontend/src/fonts/source-serif-4-400.woff2
  - frontend/src/main.tsx
  - frontend/src/registries/renderers/GapFillRenderer.module.css
  - frontend/src/registries/renderers/GapFillRenderer.tsx
  - frontend/src/registries/renderers/ProofRenderer.tsx
  - frontend/src/registries/renderers/gapFillRenderer.test.tsx
  - frontend/src/registries/renderers/proofRenderer.test.ts
  - frontend/src/registries/renderers/registry.ts
  - frontend/src/registries/renderers/stripEmphasis.ts
  - frontend/src/registries/renderers/types.ts
  - frontend/src/styles/tokens.css
  - frontend/src/vite-env.d.ts
  - pyproject.toml
  - uv.lock
covered_digest: "v2:sha256:f63015e6033ea1e1f314479530540212b600426a1ff43f98c8047c6f65bf5482"
---

# Phase 01: Mod-First Manual Learning Loop — Final Re-verification

**Result:** gaps_found, **4/5 roadmap truths verified**, one evidenced product blocker.
**Verified:** 2026-10-08T01:58:44Z. Verification-only continuation; no completed plan was re-executed.
**Implementation baseline:** d8b2611 on phase/01-execution; implementation is unchanged from 0f30388.
**Phase goal:** A learner can launch the local application and complete a source-to-feedback Gap Fill workflow, while maintainers can observe that it runs through documented public contracts.

## Scope and evidence

All 18 PLAN contracts and SUMMARY metadata/coverage were reconciled with the current five roadmap criteria, all 17 Phase 1 requirement IDs, current source and the earlier verification. CLI execution inventory has 18 summaries and zero incomplete plans. Historical plan prohibitions apply to their execution windows; later expressly approved amendments supersede incompatible presentation assertions. In particular, 01-15's no-retry/disabled-control wording and 01-16's post-reveal no-retry wording are superseded by 01-16/18 and D-34. None justifies re-executing a completed plan.

The accepted contract is R2 D-32–D-37. No Details/chunk-label teaching UI is required in Phase 1. Original full EVAL-05 remains **partial/deferred to Phase 5** and unchecked; saved raw educational data must still be retained. This is an approved specification amendment, not a claim that absent education was implemented and not an invented verification override.

New UAT is **76/76**: **14 explicit human Docker functional passes + 62 previously recorded automated coverage entries**. Tests 1–14 and the completed Manual-Only row in 01-VALIDATION.md close the separate phase learner smoke. Test 12 covers all four result states across reload, direct URL, list return, actual browser-process restart and Docker/app restart with retained volume. Test 13 covers 320px. These are user-reported results, not fresh assistant browser observations. No fresh-volume restart or live CI run is claimed; original startup evidence remains historical.

Five named checks passed in this verification and one newly reproducible invariant failed. Passing UAT does not negate an asynchronous interleaving that its checks did not exercise. The 2026-10-08 Nyquist/security audits and full backend 129/frontend 105/typecheck/build results are retained dated evidence; they were not rerun or rewritten as new passing evidence.

Roadmap mode is still mvp with a goal outside the official user-story syntax. The previous report already retained this planning discrepancy. This report checks the frozen five roadmap outcomes under the user's explicit verification-only scope; it does not claim canonical MVP user-story format validation or alter the goal.

## User Flow Coverage and Goal Achievement

| # | Roadmap outcome | Result | Evidence |
|---|---|---|---|
| 1 | Docker launch, paste, lesson list and durable reopen | VERIFIED | migrate() precedes execvp in docker/api_entrypoint.py; Compose health configuration; public lesson create/list/get persistence chain. UAT 1–3, 12 and recorded phase smoke supply missing Docker/restart evidence. |
| 2 | Source-linked accepted units, Gap Fill generation and one-item progression | FAILED — BLOCKER | Normal flow passes UAT 3–4, 8, 10–11 and named retry test. WR-02 probe demonstrates delayed submit rewinds persisted progression 2 → 0. |
| 3 | Approved inline Correct/Incorrect/Corrected, disclosure/clearing retry, full payload and exact restore | VERIFIED for narrowed acceptance | GapFillRenderer renders expected for accepted/revealed only, otherwise submitted; graded input/chips unmount, Try again is available before/after reveal. Repository/query/HTTP/generated DTO preserve saved fields; restore binds exact attempt and item; epoch guards isolate UI responses. Fresh HTTP, exact-row restore and reveal checks pass; UAT 6–7, 11–13 pass. Detailed education is explicitly deferred. This presentation verification does not certify the separate WR-02 server-ordering invariant. |
| 4 | Active diagnostics, public command/query seams, proof module and invalid-catalog rejection | VERIFIED — regression check | create_app validates catalog before serving; describe allowlists public fields; contribution visibility filtering and exercise-type renderer registry remain wired. Existing startup/proof-removal/isolation test evidence and UAT automated entries 18–21, 58–61 retained. |
| 5 | Generated OpenAPI client, CI dirty-diff gate, independent test targets | VERIFIED — regression check | Fresh named drift test passes; practiceAdvance POST/path/export/call present. CI export → pinned generator → git diff gate and separate domain/persistence/modules/application targets inspected. Existing generation-repeat evidence retained; live CI not claimed. |

Score: **4/5**, behavior-unverified truths: **0**, overrides: **0**.
No outstanding manual acceptance check is invented. One demonstrated implementation defect keeps the phase open.

## Plan reconciliation

| Plans | Current disposition |
|---|---|
| 01-01–03 | Lesson/public catalog/manual units remain implemented; UAT 1–4 and recorded module/application coverage. |
| 01-04–05 | Deterministic module, accepted-only generation and sessions implemented; WR-02 is a persistence/order defect, not an instruction to rerun these plans. |
| 01-06–07 | Workspace/focus/registry implemented. Old full-feedback presentation expectations superseded by D-32–D-37. |
| 01-08–11 | OpenAPI/independent testability/Compose/finish/start-over implemented; current named drift check passes. |
| 01-12–14 | Open-session resume, read hydration/end close and layout implemented; UAT 10, 12–14 closes current manual evidence. |
| 01-15–16 | Historical G-01-1 fixed; normal same-session retry and opening denominator pass. WR-02 now independently reproduced under overlapping requests. |
| 01-17–18 | Complete saved payload and R2 inline/restore implementation verified; final R2 approval and separate phase smoke recorded. Original EVAL-05 education remains deferred. |

## Required Artifacts, Wiring and Data Flow

| Path / chain | Result and substance |
|---|---|
| Dockerfile.api/web, docker-compose.yml, docker/api_entrypoint.py | Present and substantive; migration precedes serve and health; README documents startup. Human Docker evidence is now complete for this retained-volume learner flow. |
| CreateLessonForm / LessonListPage → lessonApi → generated client → lesson routers → application handlers → SQLite | Real lesson values feed the workspace/list; immutable raw source remains stored. |
| Source selection → learning_unit.add/accept → accepted set → registry generate → stored generation/session | Canonical code-point spans and accepted-set guards remain. Normal start/get freeze and unique-open-session behavior retained. |
| module evaluator → SubmitResult → FocusPracticeMode → GapFillRenderer | Category/reference comes from server, not client grading. Inline display gating reads actual submitted/expected values. |
| AttemptRow JSON → _saved_chunks → AttemptRecord → ListedAttempt → HTTP DTO → generated type → savedFeedback | Genuine arrays/nullability preserved, malformed data fails reads; no synthetic empty chunks. Fresh reopened HTTP test exercises rich/empty fields without DB mutation by reads. |
| local pending/reveal binding + exact listed attempt → restorePractice → captured display item | Exact session/attempt/item/position/unit/mode/span/target/segments/chip identity, successful pending item and final result restore; currentRequest epoch checks isolate late UI responses. Fresh exact-rich-row/remount test passes. |
| Continue → generated practiceAdvance → practice.advance → advance_current_item | Sequential progression works. add_attempt separately overwrites cursor from its stale read, violating the end-to-end progression invariant under overlap. |
| Validated bundled catalog → public describe/list_visible_for → module and renderer registry | Gap Fill/proof contributions use public seams; proof hidden from learner selection; invalid catalogs rejected before serving. |
| OpenAPI export → pinned generator → committed SDK → CI git diff | Current operation export/method/path and feature call inspected; weak test oracle warning WR-03 retained independently of the stronger configured CI diff gate. |

## Fresh Behavioral Checks

Backend prefix: `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider`; append the exact node below and `-q`.

| Exact check | Fresh result |
|---|---|
| backend/tests/adapters/http/test_http_dto_mapping.py::test_reopened_http_lists_complete_saved_feedback_without_mutation | PASS, 1 passed, 1.90s; deprecation warning only. Rich/empty/raw payload, exact identity and unchanged stored records asserted through new app/repository. |
| backend/tests/application/test_practice_retry.py::test_repeat_round_keeps_pair_identity_and_opening_size | PASS, 1 passed, 1.64s; real temporary migrated DB, pair identity and denominator. |
| backend/tests/adapters/http/test_openapi_client_drift.py::test_typescript_client_matches_openapi_and_ci_rejects_drift | PASS, 1 passed, 1.33s; current operation coverage/configuration, not execution of CI. |
| node frontend/node_modules/vitest/vitest.mjs run --root frontend src/features/lesson/LessonWorkspacePage.test.tsx -t 'restores actual rich payload from the exact row' --maxWorkers=1 --reporter=verbose | PASS, 1 selected, 58 filtered; 22.77s harness total. Exact row's full RendererFeedback and matching reveal survive remount without writes. |
| node frontend/node_modules/vitest/vitest.mjs run --root frontend src/registries/renderers/gapFillRenderer.test.tsx -t 'Show answer fills the blank' --maxWorkers=1 --reporter=dot | PASS, 1 selected, 15 filtered; 12.18s harness total. Inline disclosure keeps category and no commands/credit; retry remains available. |
| .venv/Scripts/python.exe -B .planning/phases/01-mod-first-manual-learning-loop/verification-evidence/wr02_cursor_probe.py | FAIL, exit 1: `WR-02: cursor before delayed submit=2, after=0; request errors=[]`; `AssertionError: PROVEN DEFECT: delayed submit rewound durable cursor from 2 to 0`. |

Frontend filtered tests are not disabled tests. Harness startup exceeded the 10s spot-check target; selected behavior itself completed promptly. No full suite or server was started.
Initial inline copies of the race probe demonstrated the same 2 → 0 defect but produced Windows temporary-DB cleanup noise. The saved reproduction disposes the engine, then fails only its invariant; its fresh output above is the authoritative evidence.

### Probe interpretation

The probe schedules two legitimate submissions to the first item. One is delayed at the persistence call after the public handler reads the item/cursor. The other returns Incorrect; an independent correction advances to item 1, and its correct answer advances to cursor 2. Releasing the delayed Incorrect request persists cursor 0. This is an allowed overlapping request schedule with deterministic barriers, not a hand-edit of learner storage. Application handlers and real migrated SQLite are exercised. Epoch guards protect browser display; they do not protect the already-executing server command.

No phase-declared probe shell scripts were discovered. The verification-only reproduction is retained for review and repeatability; no permanent test suite or production fix was added.

## Requirements Coverage

All **17** roadmap IDs appear in PLAN frontmatter; no orphaned or unknown requirement IDs.

| Requirement | Source plans | Current disposition / evidence |
|---|---|---|
| LESS-01 | 01, 06, 14 | SATISFIED: exact paste/create and UI path; UAT 2. |
| LESS-02 | 01, 06 | SATISFIED: real list/get/reopen; UAT 1–2, 12. |
| ANLY-08 | 03, 06, 14 | SATISFIED: selected occurrence, acceptance, logical remove/freeze; UAT 3, 11. |
| EXER-01 | 05, 06, 14 | SATISFIED: accepted-only generation, terminal status and ready handoff; UAT 4. |
| EXER-02 | 05, 07, 12, 13 | BLOCKED under overlapping submits: one-item durable progression can rewind, WR-02. Normal resume/start evidence remains valid. |
| EXER-03 | 04, 07, 15, 16 | SATISFIED: public Gap Fill renderer/module; UAT 4–8. |
| EXER-07 | 05, 07, 11, 13, 18 | BLOCKED under overlapping submits: subsequent session progression is not stable, WR-02. Sequential submit/feedback/Continue checks pass. |
| EVAL-01 | 04, 07, 18 | SATISFIED for Phase 1: server deterministic identity/strip+casefold rules; no browser-computed grade. |
| EVAL-04 | 04, 07 | SATISFIED for approved closed-answer scope: explicit result and corrected remap; broader categories remain representable. |
| EVAL-05 | 04, 07, 15–18 | PARTIAL / approved remainder deferred to Phase 5. Narrowed inline disclosure/restore and real payload checks pass; full education is not complete. |
| MODL-01 | 02 | SATISFIED: startup validation before serving; prior named negative catalog tests retained and source unchanged. |
| MODL-02 | 02 | SATISFIED: public active describe, contribution visibility and separate learner query. |
| MODL-03 | 02, 04, 07, 09 | SATISFIED: public proof contribution/renderer/removal seams, no core routing by module id. |
| MODL-12 | 01, 08, 09 | SATISFIED: DTO-only HTTP → documented application handlers; isolation and read query contracts retained. |
| PLAT-03 | 09, 10 | SATISFIED: migration-before-health configuration, historical fresh startup and current Docker learner smoke/restart user reports. |
| PLAT-09 | 08 | SATISFIED: current generated operation mapping and CI export/generate/diff; fresh drift test passes with WR-03 test-strength warning retained. |
| PLAT-10 | 09 | SATISFIED: independent directories/targets and handler/module seams; existing split suites retained. |

Requirement completion checkboxes/phase transition were not changed: this report is a verification verdict, not phase.complete.

## Historical Findings Reconciled

| Historical item | Current disposition |
|---|---|
| Prior truth 1 behavior-unverified / phase smoke pending | CLOSED by new UAT 1–14 and completed VALIDATION Manual-Only row, with explicit user-report attribution. |
| Prior chunk loss, synthetic [] on reopen | CLOSED by 01-17 faithful projection and 01-18 strict exact restore; fresh HTTP and exact-rich-row checks pass. |
| Prior mandatory full Details/education | SUPERSEDED current Phase 1 acceptance; approved D-32 transfer to Phase 5. Original requirement stays incomplete. |
| Historical G-01-1 options not shuffled | RESOLVED: per-session/item permutation, renderer uses received chip order; UAT 5. |
| Historical G-01-1 invisible input / editable graded control | RESOLVED current acceptance: label/border/instruction before grading, control unmounted after grading; UAT 6–7. |
| Historical G-01-1 technical Feedback log / missing score | RESOLVED original minimal criterion: Current pass, opening score and plain labels; UAT 9, 14. New compact-summary preference O-01-9 remains separate UX debt. |
| Historical G-01-1 emphasis stars/double underline | RESOLVED: presentation strips emphasis, blank has one line; immutable source untouched; UAT 2, 6. |
| O-01-10-exit starts item 1 next time | EXPECTED: Exit closes; later start opens a new pass. User explicitly passed UAT 10; not a bug. |
| WR-01 readOnly guard not re-armed on Try again | WARNING retained: answerEditable remains true across same renderer retry. No current functional acceptance failure or reproduction of unwanted autofill; not promoted to blocker. |
| WR-02 overlapping submit/Continue | ONE EVIDENCED BLOCKER: durable cursor rewind reproduced. The warning's additional double-append and closed-session-write branches were not separately reproduced or counted as additional blockers. |
| WR-03 drift test matches methods globally | WARNING retained: weak oracle is visible in code. Current SDK bindings and stronger CI generated diff inspected; no current client mismatch demonstrated. |
| 01-UI-REVIEW old 14/24 / no blockers | Historical visual report, not a fresh audit or evidence of present implementation failure. |

### UAT-HISTORY and the completion predicate

01-UAT-HISTORY-2026-10-06.md is preserved verbatim with its historical `status: diagnosed`, `result: issue`, and G-01-1 `status: resolved` / plan 01-15 resolution. Its symptoms are reconciled above against current code and UAT, not converted retroactively into pass.

The official CLI scans every immediate-directory filename containing `-UAT` and ending `.md`, so it also treats this archive as active input. `phase.uat-passed 01 --require-verification` therefore reports the historical header/test as blockers even though its gap is resolved and current UAT is 76/76. These are **archive-discovery false positives**, separate from the genuine WR-02 failure. No GSD runtime modification, archive move or force bypass was made in this verification-only continuation. Before any later phase transition, archive discovery needs honest reconciliation (preserve original bytes and references), not rewriting the old failed test as passed.

The prior canonical report is preserved in `verification-evidence/verification-2026-10-06.md`; current verdict replaces the stale canonical body.

## Test Quality, Anti-Patterns and Decision Coverage

- Relevant pytest/Vitest source scan found no actual disabled requirement test; the `handleExit(` substring match is not `xit(` test disabling. Selected skips are filters.
- HTTP preservation assertions compare rich/empty/raw values authored independently of projection, through a fresh app/repository; before/after DB snapshot checks read-only behavior. UI exact-row assertions check full payload and identity/remount, not merely existence. Normal retry assertions check state transitions on real temporary persistence.
- No unreferenced TBD/FIXME/XXX debt markers found in backend/frontend implementation. The generated client contains an upstream TODO; it is not a hollow data prop or a phase goal blocker.
- WR-02 is an existing review observation with fresh deterministic evidence; it is not an architectural preference or new unsourced scope. Current repositories.py was changed in the gap-closure period, and the invariant failure is independently reproducible.
- The original 23-decision coverage query reports 23/23 honored; its Git ownership diagnostic prevents treating it as fresh independent history verification. D-32–D-37 were directly reconciled with current source/UAT; earlier recorded R2 coverage is 6/6. These advisory counts do not override the failed runtime invariant.
- Remaining non-inferable residuals explicitly flagged/accepted in older plans are not silently certified as general concurrency/property proofs. In particular the double-submit backstop in 01-05 is contradicted by the fresh WR-02 evidence. 320px visual result is now supplied by user UAT 13. No claims of paid AI, broad browser automation, live CI or fresh-volume destruction.

## Remaining Actual Blockers

**One product blocker: G-01-VER-20261008-WR02.** Delayed submit rewinds stored cursor 2 → 0 at repositories.py:431, disrupting one-item practice progression. The current phase cannot receive passed until a fix and passing regression evidence close this invariant.

O-01-9 is a concrete UX request whose ownership remains undecided, **not an automatic blocker**. Full EVAL-05 education is an approved Phase 5 deferral, **not a Phase 1 blocker**. Historical UAT discovery is an administrative predicate problem, **not a revived implementation gap**. No outstanding human test remains under the approved Phase 1 contract.

No application edits, completed-plan reruns, phase.complete, new gap planning, commit or push were performed. The next implementation entry point, if requested, is `$gsd-plan-phase 01 --gaps`, targeting this single evidenced invariant while retaining all passed R2/UAT evidence.
