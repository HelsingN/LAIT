---
phase: 01-mod-first-manual-learning-loop
verified: 2026-10-08T02:29:12Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
scope_revision: "01-18 R2; D-32–D-37; 01-19 WR-02"
scope_narrowing_approved: true
original_eval05_status: partial_deferred
uat_status: complete
uat_passed: 76
uat_human_passed: 14
uat_recorded_automated_passed: 62
phase_completion_performed: true
phase_closed: 2026-10-08T03:14:12Z
metadata_reconciled: 2026-10-08T16:59:59Z
re_verification:
  previous_status: gaps_found
  previous_score: "4/5"
  previous_verified: "2026-10-08T01:58:44Z"
  gaps_closed:
    - "WR-02: delayed accepted submit cannot restore an earlier cursor; cursor 2 remains exactly 2 on response/current/new repository reads."
    - "Associated overlap branches: final retry append occurs once; a delayed submit losing to Exit cannot append to closed history."
  gaps_remaining: []
  regressions: []
gaps: []
deferred:
  - truth: "Original full EVAL-05 educational explanation, target-chunk analysis and optional natural-alternative presentation within the session."
    addressed_in: "Phase 5"
    evidence: "Approved 01-18-CONTEXT.md D-32–D-37, ROADMAP criterion 3 and REQUIREMENTS.md EVAL-05; reiterated by user."
advisory:
  - finding: "O-01-9-visual: compact workspace Feedback requested."
    category: other
    reason: "Functional UAT passes. UX/visual debt; Phase 9 proposed, not approved."
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
  - .planning/phases/01-mod-first-manual-learning-loop/01-19-PLAN-CHECK.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-19-PLAN.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-19-SUMMARY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-CLOSURE.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-CONTEXT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-PATTERNS.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-REVIEW-DISPOSITION.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-REVIEW.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-SECURITY.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-UAT.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-UI-REVIEW.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-VALIDATION.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/.gitattributes
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-PATTERNS-2026-10-07.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-REVIEW-2026-10-02.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-REVIEW-2026-10-06.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-REVIEW-DISPOSITION-2026-10-02.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-REVIEW-DISPOSITION-2026-10-06.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-UAT-HISTORY-2026-10-06.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/01-UI-REVIEW-2026-10-06.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/README.md
  - .planning/phases/01-mod-first-manual-learning-loop/history/audit-archive-index.json
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
covered_digest: "v2:sha256:46ffda1418b7d564b597dbd87aad16c2e35958920b0680dc0f5fdc1e48c16331"
---

# Phase 01: Mod-First Manual Learning Loop — Final Re-verification

**Result: passed, 5/5 roadmap truths verified.** Zero remaining evidenced implementation blockers, zero behavior-unverified truths, zero overrides.
**Verified:** 2026-10-08T02:29:12Z. Production baseline: `d6abcc6`; plan/summary closeout: `e7fbe65`, branch phase/01-execution.
**Phase goal:** A learner can launch the local application and complete a source-to-feedback Gap Fill workflow, while maintainers can observe that it runs through documented public contracts.

## Scope and evidence

All 18 previously completed PLAN/SUMMARY contracts were retained and reconciled; only the newly authorized backend gap plan **01-19** executed. Current official execution inventory: 19 plans, 19 summaries, zero incomplete/runnable plans, zero duplicate threat IDs. The report covers current implementation and 239 versioned files with the official v2 content fingerprint, including preserved UAT history and formal closure evidence. Regenerable frontend/openapi.json is deliberately gitignored and excluded from portable fingerprint inputs; the tracked exporter, generated SDK, operation tests and CI generation/diff configuration remain covered.

Current UAT is **76/76**, comprising 14 explicit user-reported functional Docker passes and 62 recorded automated coverage entries. Completed phase Docker learner smoke and the approved 01-18 R2 checkpoint remain valid evidence; this run adds no new manual/browser/Docker observation. Backend-only 01-19 changes no UI, schema, DTO, dependency or learner database, so no new blocking-human checkpoint applies.

D-32–D-37 remain the accepted Phase 1 scope. Full original EVAL-05 education/chunk/alternative presentation stays **partial/deferred to Phase 5**, not declared delivered. The subsequent user-authorized administrative closeout archived historical UAT byte-for-byte and ran official phase.complete on 2026-10-08: 19/19 plans, Phase 2 ready to plan. No completed-plan rerun or Phase 2 implementation. Details: [01-CLOSURE.md](./01-CLOSURE.md).

## Observable Truths

| # | Roadmap truth | Verdict and evidence |
|---|---|---|
| 1 | Health-checked Docker launch, English paste and lesson reopen | VERIFIED. Migration-before-serve/health contracts unchanged; prior deployment evidence and user Docker UAT 1–2, 12, 14 retained. Fresh persistence/reopen group passes. |
| 2 | Source-linked accepted unit, Gap Fill generation and one-item completion | VERIFIED. Prior accepted-only generation/UAT 3–8 retained. Fresh 01-19 delayed Incorrect and Correct captured at 0 remain at exactly 2 after independent progression, including new database reads. Replay retains a distinct attempt without re-advancing; final retry round appended once. |
| 3 | Approved deterministic inline result, reveal/clearing retry, Continue and exact saved payload restore | VERIFIED under D-32–D-37. Existing user four-state × five-route UAT 12, narrow-screen UAT 13 and final checkpoint retained. Fresh Focus/Workspace/Feedback 69 passes plus HTTP/read/backend retry checks preserve exact saved fields, opening denominator, pair identity, Corrected and Exit/Start Over. |
| 4 | Public diagnostics, commands/queries, proof registry seams and invalid-catalog rejection | VERIFIED. Current wiring remains unchanged; earlier named startup/catalog/proof tests and UAT 18–21, 58–61 retained. Fresh handler-isolation tests pass; HTTP layer remains DTO-only. |
| 5 | Generated OpenAPI client, CI dirty-diff detection and independent targets | VERIFIED. Earlier named October 8 drift check and generation-repeat evidence retained. No transport/schema change in 01-19. SDK practiceAdvance binding, CI export/generate/diff and split targets remain unchanged; live CI is not claimed. |

## Plan reconciliation and wiring

| Plans / chain | Current disposition |
|---|---|
| 01-01–03 | Lesson/public catalog/manual units implemented; UAT 1–4 and retained module/application evidence. |
| 01-04–05 | Deterministic module/accepted-only generation/session implemented; the persistence ordering defect was repaired in new 01-19. |
| 01-06–07 | Workspace/focus/registry implemented. Original full-feedback presentation expectations superseded by approved D-32–D-37. |
| 01-08–11 | OpenAPI/split testability/Compose/finish/start-over implemented; affected regressions pass. |
| 01-12–14 | Resume/read hydration/end close/layout implemented; UAT 10, 12–14 and fresh reopen tests. |
| 01-15–16 | Historical G-01-1 resolved; same-session repeat identity, corrected exclusion and opening denominator pass. |
| 01-17–18 | Complete real payload and exact inline/restore implementation retained; user approval plus phase smoke recorded. Full education deferred. |
| 01-19 | Completed newly authorized WR-02 fix and regression verification, production commit d6abcc6. |
| lessonApi → generated SDK → HTTP DTOs → application commands → repository | Public seams preserved. Production change is private persistence locking plus authoritative SubmitResult.cursor, with no field/signature change. |
| evaluator → add_attempt → advance_current_item → stored session | add_attempt accepts a distinct immutable attempt without assigning captured cursor. Open-status no-op UPDATE acquires the database write lock before reading session progression. Advancement guards captured position under that transaction; already-passed positions return current cursor. |
| final position → still-uncorrected pairs → appended retry items | Check/read/append occurs inside the serialized transaction. Concurrent final Continue calls observe the winner's cursor and append only one round. Pair identity and initial denominator unchanged. |
| Exit → late insert | Open-status check occurs under the write lock. When Exit already won, insertion is rejected and closed history is unchanged. Accepted earlier attempts remain intact. |
| AttemptRow JSON → saved projections → HTTP → generated types → exact savedFeedback | Existing genuine arrays/nullability/identity and read-only preservation retained. No synthetic feedback added. React epoch guards still protect presentation; durable progression now has an independent backend guard. |
| OpenAPI export → pinned generator → committed SDK → CI diff | Existing configuration and operation mapping unchanged; WR-03 weak test oracle remains advisory alongside the stronger generated-diff gate. |

## Fresh behavioral checks

| Exact check / scope | Result |
|---|---|
| New tests selected on old implementation: retry file, -k 'delayed_submit or replayed_named or overlapping_final' | RED: 4 failed, 1 passed, 4 deselected. Incorrect 2→0; Correct 2→1; duplicate appended retry item; late attempt inserted after Exit. Named replay already passed. |
| backend/tests/application/test_practice_retry.py | GREEN: 9 passed, final post-format run 3.14s. Delayed False/True cases assert response/stored/public query/new repository cursor exactly 2. |
| Affected submit/start/finish/reopen/isolation/persistence/HTTP group | GREEN: 48 passed, 10.54s; HTTPX/Starlette deprecation warning only. Exact paths and command recorded in 01-VALIDATION.md. |
| node frontend/node_modules/vitest/vitest.mjs run --root frontend src/features/lesson/FocusPracticeMode.test.tsx src/features/lesson/LessonWorkspacePage.test.tsx src/features/lesson/stages/FeedbackStage.test.tsx --maxWorkers=1 --reporter=dot | GREEN: 69 passed, 3 files, 19.43s. |
| .venv/Scripts/python.exe -B .planning/phases/01-mod-first-manual-learning-loop/verification-evidence/wr02_cursor_probe.py | PASS exit 0: cursor before delayed submit=2, after=2; request errors=[]. |
| Ruff check --no-cache / format --check on three changed backend files | PASS; 3 files already formatted. |
| git diff --check | PASS. |

Total **57 affected backend + 69 affected frontend passes**. This is not a fresh full-suite run. Previously passing named October 8 payload/remount/reveal/OpenAPI checks are retained; HTTP/workspace groups freshly include the affected saved-feedback checks. Tests and the probe use newly migrated temporary SQLite, not the learner volume. No fresh-volume deletion, paid AI call, server or browser automation.

### Regression quality and WR-02 disposition

The delayed test pauses at add_attempt after the public handler captured position 0. Independent handlers produce Incorrect, Corrected and then a correct next answer to reach cursor 2. Releasing either old Incorrect or Correct leaves **2 exactly**, rather than merely asserting a nondecreasing cursor. A newly opened repository and public practice.get independently read position 2; all four accepted attempts are distinct, earlier rows unchanged, initial denominator 4.

Replay of a named old target retains a third attempt with cursor 2. Two synchronized final-position Continue requests both return cursor 1 and a fresh repository reads exactly positions [0,1], one appended copy of the still-missed pair. A request delayed before insertion loses to Exit and raises PracticeSessionNotFoundError; fresh reads retain the closed session and only the earlier accepted attempt. New race schedules fail for four branches on old code and pass after the fix. PostgreSQL row-lock behavior is not runtime-certified by these SQLite tests.

## Requirements coverage

All **17** roadmap IDs occur in PLAN frontmatter; no orphaned/unknown IDs. Previous source-plan mapping retained; 01-19 additionally covers EXER-02/EXER-07.

| Requirement | Current disposition / evidence |
|---|---|
| LESS-01 | SATISFIED: exact paste/create; UAT 2 and retained named tests. |
| LESS-02 | SATISFIED: list/get/reopen; UAT 1–2,12 and fresh reopen group. |
| ANLY-08 | SATISFIED: selected occurrence/accept/remove/freeze; UAT 3,11 and retained tests. |
| EXER-01 | SATISFIED: accepted-only generation and ready handoff; UAT 4 and retained generation tests. |
| EXER-02 | SATISFIED: normal one-item/resume plus fresh delayed-submit cursor 2 invariants and start tests; 01-19 closes WR-02. |
| EXER-03 | SATISFIED: public Gap Fill module/renderer; UAT 4–8 and retained module tests. |
| EXER-07 | SATISFIED: fresh retry/submit/finish/Start Over/Continue, replay, serialized append, closed-history and UI groups. |
| EVAL-01 | SATISFIED for Phase 1: server deterministic identity and strip+casefold; fresh submit tests, existing evaluator evidence. |
| EVAL-04 | SATISFIED for approved closed-answer scope: explicit Correct/Incorrect/Corrected; fresh affected checks. |
| EVAL-05 | PARTIAL; approved original education remainder deferred to Phase 5. Narrowed inline disclosure/restore and full payload pass. |
| MODL-01 | SATISFIED: startup validation before serving; retained negative catalog tests/source unchanged. |
| MODL-02 | SATISFIED: public active describe/visibility query; source and UAT retained. |
| MODL-03 | SATISFIED: public proof contribution/renderer/removal; source and proof evidence retained. |
| MODL-12 | SATISFIED: DTO-only HTTP/public handlers, fresh isolation and HTTP/read tests. |
| PLAT-03 | SATISFIED: migration-before-health config, prior startup and current user-reported Docker smoke/restart; fresh persistence contract tests. |
| PLAT-09 | SATISFIED: unchanged SDK operation/CI generation diff; earlier October 8 named drift check retained. WR-03 advisory remains. |
| PLAT-10 | SATISFIED: independent directories/targets; fresh isolation and affected persistence checks. |

No phase-level requirement checkbox was silently advanced by this verification verdict. Full EVAL-05 is not checked complete.

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
| WR-02 overlapping submit/Continue | CLOSED by 01-19: delayed Incorrect/Correct now preserve 2, including fresh repository; named replay does not advance. Additional final-round double append and late closed-session history branches reproduced RED and fixed GREEN. |
| WR-03 drift test matches methods globally | WARNING retained: weak oracle is visible in code. Current SDK bindings and stronger CI generated diff inspected; no current client mismatch demonstrated. |
| 01-UI-REVIEW old 14/24 / no blockers | [October 6 original](./history/01-UI-REVIEW-2026-10-06.md) archived byte-for-byte; stable current path indexes it. Historical visual report, not a fresh audit or evidence of present implementation failure. |

### UAT-HISTORY and the completion predicate

[history/01-UAT-HISTORY-2026-10-06.md](./history/01-UAT-HISTORY-2026-10-06.md) is preserved verbatim with its historical `status: diagnosed`, `result: issue`, and G-01-1 `status: resolved` / plan 01-15 resolution. Its symptoms are reconciled above against current code and UAT, not converted retroactively into pass.

The official CLI scans immediate-directory filenames containing `-UAT` and ending `.md`. On 2026-10-08 the historical archive was moved into phase-local `history/`; current UAT links resolve there. Before/after SHA-256 is `DD8DEA68E6D76754BA95184D659D6B2D798A7018E368E0829ABFFFB613578818`. The old false-positive header/test blockers are therefore removed from active discovery without changing archived bytes, failed rows, GSD runtime or acceptance policy. Current `phase.uat-passed 01 --require-verification` is rechecked after the metadata fingerprint refresh. Original plan 01-19 evidence remains dated; this administrative closeout adds no implementation or manual acceptance claim.

The prior canonical reports are preserved in `verification-evidence/verification-2026-10-06.md` and `verification-evidence/verification-2026-10-08-wr02.md`. Current verdict replaces the stale canonical body.

### Historical review/pattern/UI archive reconciliation

Quick task 261008-rko preserves four local pre-closeout reports and the two earlier tracked October 2 review/ledger versions as dated snapshots. [history/README.md](./history/README.md) and [audit-archive-index.json](./history/audit-archive-index.json) identify each source and SHA-256; history attributes preserve original line endings through Git checkout. Old statuses, findings and UI score remain unchanged in the archives.

[Current review](./01-REVIEW.md) and [disposition](./01-REVIEW-DISPOSITION.md) use October 6 meanings explicitly: WR-02 fixed by 01-19; WR-01/WR-03 remain open nonblocking advisories without an invented approved deferral. October 2 IDs have different titles and are retained separately, not silently reused or retrospectively passed. Stable [PATTERNS](./01-PATTERNS.md) and [UI-REVIEW](./01-UI-REVIEW.md) paths keep completed-plan/UAT references resolving while identifying D-32–D-37 supersession. No implementation test, fresh code/UI audit, scope/requirement change or completed-plan rerun accompanies this metadata reconciliation. Phase 1 acceptance remains passed 5/5, UAT 76/76, and original full EVAL-05 remains partial/deferred to Phase 5.


## Test quality, threats and limits

T-01-51 mitigation is closed after source review and fresh barrier-controlled tests: cursor-neutral inserts, serialized open-session writes and captured-position progression. Register now 58 threats, 52 closed, 6 accepted, zero open blocking; prior ASVS evidence retained, no new full ASVS audit claimed.

Prior anti-pattern/disabled-test/source scans remain valid for unchanged code. New tests invoke public handlers and real persistence, assert independent values and new-reader durability, compare old attempt rows, and cover rejection after a terminal transition. No skip/watch/xfail introduced. No broad property proof or future distributed-worker guarantee is inferred.

WR-01 readOnly retry guard and WR-03 weak drift-test oracle remain warnings, with no current accepted-flow failure. O-01-9 compact Feedback remains concrete UX debt with ownership undecided. Raw historical UAT is preserved, not converted into an acceptance override.

## Remaining actual blockers

**No remaining evidenced product blocker. Canonical verdict: passed, 5/5.** WR-02 is closed by implementation and fresh regression evidence; original EVAL-05 is an approved Phase 5 deferral.

The administrative archive-discovery problem is resolved by the byte-preserving move into `history/` and current link update. UAT 76/76 and the existing phase smoke are retained; no new human test is pending under current Phase 1/backend-only scope. Subsequent official phase.complete succeeded after the passing predicate; no force bypass or original EVAL-05 completion. One nonblocking command-as-file metadata warning is recorded in 01-CLOSURE.md.
