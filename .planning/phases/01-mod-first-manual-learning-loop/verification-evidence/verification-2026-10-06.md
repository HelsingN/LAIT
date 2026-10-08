---
phase: 01-mod-first-manual-learning-loop
verified: 2026-10-06T20:52:32Z
acceptance_amended: 2026-10-07
scope_revision: "01-18 R2; D-32–D-37"
scope_narrowing_approved: true
original_eval05_status: partial_deferred
repeated_checkpoint_approval: approved
repeated_checkpoint_approval_date: 2026-10-07
repeated_checkpoint_approval_source: user_report
status: gaps_found
score: 3/5 must-haves verified
behavior_unverified: 1
overrides_applied: 0
nyquist_compliant: false
decision_coverage:
  honored: 23
  total: 23
  not_honored: []
re_verification:
  previous_status: gaps_found
  previous_score: "2/5"
  previous_verified: "2026-10-06T17:32:54Z"
  gaps_closed:
    - "Maintainer can generate the TypeScript client from OpenAPI, have CI detect an unreviewed contract/client mismatch, and test the core, persistence adapter, and bundled modules independently."
  gaps_remaining:
    - "Original full EVAL-05 remains incomplete: detailed teaching/chunk/alternative presentation explicitly deferred to Phase 5 by D-32–D-37. Narrowed Phase 1 R2 checkpoint approved by user on 2026-10-07; separate phase smoke and re-verification pending."
  regressions: []
covered_files:
  - .dockerignore
  - .env.example
  - .github/workflows/ci.yml
  - .gitignore
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
  - .python-version
  - AGENTS.md
  - Dockerfile.api
  - Dockerfile.web
  - README.md
  - backend/.dockerignore
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
  - docker/api_entrypoint.py
  - docker/web-nginx.conf
  - frontend/.dockerignore
  - frontend/index.html
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
  - frontend/tsconfig.app.json
  - frontend/tsconfig.json
  - frontend/vite.config.ts
  - pyproject.toml
  - tsconfig.json
  - uv.lock
covered_digest: "v2:sha256:fccdac6e913b202923d6371f08fde34a531e94eda4ed97dd16386289e59ae0a1"
behavior_unverified_items:
  - truth: "Learner can start the health-checked application with Docker Compose, paste English text into a lesson, and reopen that lesson from the local lesson list."
    test: "Verify fresh-volume Compose migrate-then-health separately from the required volume-kept phase learner smoke. Paste a lesson, reopen via the list, reload, navigate directly, restart the actual browser process, and restart Docker/app without deleting the volume."
    expected: "Health becomes available after migrations; source, accepted units, generation and session state reopen correctly through the relevant navigation and restart paths."
    why_human: "The passing entrypoint test monkeypatches os.execvp; it does not launch Compose. No completed phase-level Docker smoke or real browser-process restart evidence was found. Plan 01-15/16 approvals do not close this phase gate."
gaps:
  - truth: "Learner receives submitted once plus complete meaningful explanation, actual target chunks and optional natural alternative within the session; incorrect solutions remain hidden until Show answer or self-produced success, and real saved feedback restores for the exact item/attempt."
    status: failed
    reason: "Historical implementation evidence still shows no explanation/chunk/alternative consumer, no submitted display for correct results, and synthetic empty resume arrays. Reference hiding on incorrect is now required, not a defect. The approved disclosure-safe Details and exact saved-data restoration contract remains unimplemented/unverified."
    artifacts:
      - path: frontend/src/registries/renderers/GapFillRenderer.tsx
        issue: "FeedbackCard lines 172-190 does not read the required explanation/chunk fields; submitted and reference are conditional."
      - path: frontend/src/features/lesson/LessonWorkspacePage.tsx
        issue: "Lines 201-202 restore empty chunk arrays; focused && session at line 486 replaces the workspace with FocusPracticeMode."
      - path: backend/lait/application/queries/attempt_list_for_lesson.py
        issue: "ListedAttempt omits chunks_used, chunks_missed and natural_alternative despite their persistence in AttemptRow."
      - path: backend/lait/modules/exercise_gap_fill/feedback.py
        issue: "Incorrect explanation only repeats the submitted answer; the reference and missed chunk are separate payload fields not rendered by the card."
    missing:
      - "Show submitted once for every outcome; provide meaningful explanation and actual chunk associations through accessible collapsed Details without duplicate answer mentions or lost educational prose."
      - "Gate incorrect reference and all solution-bearing Details until Show answer or self-produced correct/corrected; opening Details alone cannot reveal them. Preserve legacy educational content with presentation-only compatibility."
      - "Preserve full saved feedback through repository/query/HTTP/generated client/UI restore instead of synthetic empty data, with exact item/attempt binding and stale-reveal rejection."
      - "Run planned behavioral regressions and obtain blocking Docker approval, including real browser/app restarts with volume kept; separate phase smoke remains pending."
---

# Phase 1: Mod-First Manual Learning Loop Verification Report

## Current acceptance revision — 2026-10-07, R2 checkpoint approved

Latest authority: `01-18-CONTEXT.md` D-32–D-37 and revised `01-18-PLAN.md`. The user explicitly did **not** approve the first checkpoint. This is an intentional Phase 1 scope narrowing, not a claim that the original full EVAL-05 has been implemented. Detailed educational explanation, used/missed chunk analysis and optional alternative presentation are deferred to Phase 5. No LLM or new explanation templates in Phase 1. The original EVAL-05 checkbox remains open with partial/deferred traceability.

Assess narrowed Phase 1 truth 3 as follows: Correct/Corrected fills the current blank once with the accepted reference in green and category text, without a separate answer card or duplicate graded input/chip bank. Incorrect shows submitted inline; only Show answer fills the reference while leaving Incorrect unchanged. Try again clears response/result before or after reveal. Details and technical chunk labels are absent. Existing retry rounds, corrected exclusion, Continue, opening score, Start Over and Exit remain frozen.

01-17/01-18 durable fixes are retained: complete actual explanation/chunks/nullable alternative still cross repository/query/HTTP/generated client/UI restore; no synthetic []/null. Exact attempt/copy binding, pending final-success display, strict read errors and stale-reveal/late-response guards remain required. Deferred display is not data deletion. Shared multi-blank tasks and actual drag-and-drop are recorded only in `01-18-FOLLOWUPS.md`, proposed Phase 4/9 follow-up.

All subsequent historical D-24–D-31 full-Details assertions/evidence describe the prior contract, now superseded only in content/presentation by this explicit amendment. They must not drive new Phase 1 detailed-content work or be counted as current passes. Historical verified timestamp, gaps_found status, score 3/5, truth-1 behavior abstention and phase smoke stay unchanged pending a new phase verification. PLAT-09 remains closed. Repeated R2 blocking-human Docker checkpoint is approved by the user's 2026-10-07 report: “ручная проверка пройдена без замечаний approved.” Approval/checklist attribution belongs in VALIDATION/CHECKPOINT/SUMMARY; it is not inferred from tests or design agreement. Separate phase smoke remains pending; no phase completion or Git mutation performed. Subsequent explicit Да authorizes scoped commit/push only; separate phase smoke and phase closure remain pending.

**Phase Goal:** A learner can launch the local application and complete a source-to-feedback Gap Fill workflow, while maintainers can observe that it runs through documented public contracts.
**Verified:** 2026-10-06T20:52:32Z
**Status:** gaps_found
**Re-verification:** Yes — current workspace checked against the two gaps from 2026-10-06T17:32:54Z.

One gap closed, one remains; score improved from **2/5 to 3/5**, with one additional truth present but behavior-unverified. No completed truth was reverted. Phase 1 remains incomplete. This verifier changed only this report; no fixes, plans, commits, or phase-completion writes were made.

## Scope and Contract

The historical re-verification used the previous five roadmap success criteria. Truth 3's future acceptance is clarified below by approved D-24–D-31; the recorded evidence, score and verified timestamp are not refreshed by planning. Failed items received code, wiring, data-flow and named-test checks; previously verified outcomes received regression checks. All 16 PLAN/SUMMARY pairs, roadmap, requirements, STATE, prior verification, governance and current review/validation artifacts were inspected. SUMMARY narration and checkpoint approvals are not substitutes for implementation or phase-level behavioral evidence.

Roadmap still says `mode: mvp`, but its goal fails the official `user-story.validate` form check. This is a retained specification warning, not a claim that canonical MVP user-story verification passed; this re-verification uses the previous roadmap contract and does not alter the goal or plans.

`01-VALIDATION.md` now has `status: validated` / `nyquist_compliant: true` and a PLAT-09 closure addendum, while its older audit text still describes the former drift failure. The prior claim that its current header is draft is superseded. This report does not independently certify Nyquist compliance: its Manual-Only table still lacks a completed phase learner smoke. `01-SECURITY.md` records verified / zero open threats; that is retained report metadata, not a fresh security audit.

## Approved Acceptance Amendment — 2026-10-07 (Planning Only)

Authority: `01-17-CONTEXT.md`, approved D-24–D-31. EVAL-05 and roadmap truth 3 now mean full educational feedback available **within** the session through a compact card and initially collapsed keyboard-accessible Details, with submitted displayed verbatim once for correct/incorrect/corrected. Incorrect reference and all solution-bearing explanation/chunks/alternative are withheld until Show answer or the learner's own correct/corrected answer; Details alone never reveals them. Identical submitted/reference, including text injected in saved explanations, is counted once. Compatibility presentation must handle saved legacy answer-echo templates without overwriting the original content. Meaningful deterministic explanation and actual target-chunk information remain required, not reduced.

Full saved explanation, chunks_used/chunks_missed and nullable natural alternative must survive repository reopen → application query → HTTP → generated client → UI restore. Genuine stored empty arrays/null remain valid; synthetic empty substitutes do not. Restore selects the exact attempt and item copy, not the latest session/span/mode result. Persisted Show answer is bound to item plus attempt; stale/legacy flags fail closed, while a genuine matching reveal survives all entry/restart paths on the same browser profile. Details and parameterless Show answer create zero domain mutations. Existing retry rounds, corrected semantics, opening score, Continue, Start Over and Exit remain frozen.

This is an approved acceptance clarification under D-30, **not** a verification override, implementation result or approval of new behavior. Historical observations, report timestamp, `status: gaps_found`, score **3/5**, behavior-unverified truth 1 and the open EVAL-05 gap remain intact. The dated immediate-copy assumptions in the evidence below describe the checked implementation; they do not override the newer disclosure contract. PLAT-09 remains closed; feedback DTO regeneration in 01-17 is upkeep only. No old plan is rewritten.

Planned closure: `01-17-PLAN.md` (saved-feedback contract, wave 12) → `01-18-PLAN.md` (presentation and restore, wave 13, final Docker blocking-human checkpoint). Automatic round-trip/disclosure/legacy/identity-race/regression checks and every required Docker entry/restart route are planned, **not run**. The separate phase-close learner-flow smoke remains pending in `01-VALIDATION.md`; plan approval alone cannot close the phase. No broad probe warning is promoted to another gap; traceable dispositions are in `01-17-EDGE-DISPOSITION.md`.

The historical “Feedback contract decision” manual item below is satisfied as a specification decision by this approved contract only. Its implementation and manual evidence remain pending; no reduced-content override is proposed or accepted.

## User Flow Coverage

These are the frozen roadmap outcomes, not a newly validated user-story contract.

| Step | Expected | Current code/test evidence | Status |
|---|---|---|---|
| Launch, paste and reopen | Compose migrates before health, durable lesson reopens | Entrypoint calls migrate then execvp; healthcheck and lesson routes/query/repository chain exist. Named entrypoint test passes, but substitutes execvp. | UNCERTAIN — WARNING; PRESENT_BEHAVIOR_UNVERIFIED |
| Capture, accept and practice | Source span becomes accepted unit; generation and one-item progression work | Named retry test creates a real temporary migrated repository, creates/adds/accepts/generates/starts via public handlers, submits, advances and finishes. | VERIFIED |
| Read feedback and Continue | Submitted once; full EVAL-05 education accessible under the approved disclosure gate without leaving the session | Submit computes/persists fields; FeedbackCard omits explanation/chunks and correct submitted. Incorrect reference hiding is intended; full safe Details/restore remain missing. | FAILED — BLOCKER |
| Inspect and extend contracts | Public describe, proof seam, invalid-catalog rejection | Public catalog query/renderer registrations and startup validation remain wired; named duplicate-ID rejection passes. | VERIFIED |
| Use generated transport and split tests | Current OpenAPI operations in SDK; generate-and-diff CI; independent tests | practiceAdvance export, types, re-export and feature use present; named drift and handler-isolation tests pass. | VERIFIED |

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Learner can start the health-checked application with Docker Compose, paste English text into a lesson, and reopen that lesson from the local lesson list. | UNCERTAIN (WARNING): PRESENT_BEHAVIOR_UNVERIFIED | Real lesson create/list/get adapters and routes exist. Entrypoint ordering passes in a monkeypatched process test. Actual Compose learner flow/restarts are not proven. |
| 2 | Learner can manually add and accept a source-linked learning unit, generate a Gap Fill exercise from it, and complete the exercise one item at a time. | VERIFIED | Regression inspection plus passing named retry test exercises production commands and real temporary SQLite persistence, including accept/generate/start, missed attempts, correction, advance idempotency and finish/history. |
| 3 | Learner receives submitted once and full meaningful educational Details within the session, with incorrect solution disclosure only after Show answer/self-produced success and faithful item/attempt-bound saved-data restoration (D-24–D-31). | FAILED (BLOCKER) | Historical GapFillRenderer.tsx:172-190 reads only category, conditional submitted and revealed expected; correct submitted and educational Details are absent, and resume loses chunks. The approved timing clarification is not a content override or new verification pass. |
| 4 | Maintainer can inspect active modules and capabilities, invoke the workflow through documented commands and queries, add a proof exercise contribution through the public registry and renderer seams without changing core domain services, and see startup reject invalid or incompatible module catalogs. | VERIFIED | validate_catalog runs before routers; public allowlisted describe and visibility-filtered contributions exist; proof and gap-fill use the registry; startup duplicate-ID test passes. Previous public proof seam evidence retained with basic regression inspection. |
| 5 | Maintainer can generate the TypeScript client from OpenAPI, have CI detect an unreviewed contract/client mismatch, and test the core, persistence adapter, and bundled modules independently. | VERIFIED | Live practice.advance router -> generated practiceAdvance POST/types/index -> lessonApi.advancePractice -> Continue. Named live-schema drift check and independent handler-isolation test pass; CI generation/diff and split test steps remain. |

**Score:** 3/5 truths verified; **behavior_unverified: 1**. No overrides applied. No specific coincidental-reliance precondition was found in the scored evidence: temporary databases supply ordinary caller inputs, and migration/acceptance/order are established by production commands.

### Re-verification Disposition

- **Closed:** Former generated-client gap. Current uncommitted SDK exports `practiceAdvance`, including the correct POST path, request/response types and index re-export. `lessonApi.advancePractice` calls it instead of a handwritten fetch/client.post. The named drift check now passes.
- **Remaining:** EVAL-05 in-session content and resume data loss. This is the carried-forward gap, not a newly introduced or historical-debug finding.
- **Regressions:** None identified in the previously passed outcomes under the scoped checks.
- **Deferred:** None. Later feedback/semantic-evaluation and deployment-hardening phases do not specifically defer the Phase 1 EVAL-05 contract.
- **Resolved UAT:** G-01-1 is resolved. The stale `diagnosed` UAT header and historical debug are not fresh unresolved evidence. Plan 01-15/16 approvals remain scoped to their checkpoints.

### Advisory (New Scope, Unevidenced)

None. Existing WR-01/02/03 warnings are retained below, not promoted into new-scope blockers.

### Required Artifacts — Existence, Substance and Wiring

| Artifact | Expected | Status | Details |
|---|---|---|---|
| docker-compose.yml; Dockerfile.api/web; docker/api_entrypoint.py | Local migrate-then-health deployment | Present/substantive/wired; runtime WARNING | Named entrypoint ordering passes; no actual Compose startup claimed. |
| App.tsx; LessonListPage; LessonWorkspacePage; lesson routers/commands/repositories | Durable source/list/workspace | VERIFIED at code/data-flow level | Real generated calls and SQLite reads/writes; restart acceptance remains human-needed. |
| learning_unit_add/accept; exercise_generate; practice commands | Public manual learning loop | VERIFIED | Retry test invokes production flow with real migrated temporary persistence. |
| GapFillRenderer.tsx; FocusPracticeMode.tsx | Full in-session feedback | FAILED for EVAL-05 | Component is substantive UI, not an empty stub. Required fields have no rendered consumer. |
| attempt_list_for_lesson.py; practice.py history DTO; resume mapping | Persisted feedback recovery | PARTIAL | Attempts are real; chunk fields are omitted from DTO and replaced with [] on resume. |
| generated/sdk.gen.ts, types.gen.ts, index.ts; lessonApi.ts | Generated practice.advance operation and use | VERIFIED | Export at sdk line 122; matching POST URL, typed body/path, re-export and feature call at lessonApi lines 281-288. |
| app.py; catalog validation/public query; registry.ts; proof contribution/renderer | Public seams and startup gate | VERIFIED | Catalog validated before serve; gap-fill/proof registered; describe allowlists public fields. |
| ci.yml; openapi-generate.mjs; openapi-ts.config.ts | Reproducible generator, dirty-diff gate, independent tests | VERIFIED as configured | Pinned @hey-api/openapi-ts 0.99.0; CI exports schema, generates and fails dirty generated diff. CI itself was not executed here. |

Official artifact checks: plan 01-07 returned 4/4 for file presence/patterns; that does not prove EVAL-05 behavior. Plan 01-08 returned 2/3 because `generated/` is a directory, not a file. Its key-link query returned 0/2 for symbolic sources `FastAPI app` and `openapi.json`. These are checker-input limitations, not missing SDK artifacts; the concrete implementation links were manually traced.

### Key Link Verification

| From | To | Via | Status | Evidence |
|---|---|---|---|---|
| Create/open lesson | lesson.create/list/get | generated calls -> router -> handler -> repository | WIRED | Genuine persisted source/list rows feed UI. |
| Accepted units | Gap Fill definitions | exercise.generate -> registry contribution -> repository | WIRED | Accepted-only production generation remains; retry setup exercises it. |
| Focus submit | exercise.submit_attempt | generated SDK -> handler/module evaluator -> AttemptRow | WIRED | Response includes explanation/chunk fields; payload test passes. |
| Continue | practice.advance | lessonApi -> practiceAdvance -> POST /api/practice-sessions/{session_id}/advance | WIRED | Concrete method/path/types/import/use inspected; prior handwritten-call gap closed. |
| Submit fields | in-session feedback | RendererFeedback props -> FeedbackCard | NOT_WIRED for required fields | explanation/chunks/non-null alternative are never read by card. |
| Stored attempt | resumed feedback | list DTO -> LessonWorkspacePage | PARTIAL | Chunk fields discarded; hardcoded empty arrays at lines 201-202. |
| create_app | catalog rejection | validate_catalog before routers | WIRED | Named duplicate-ID rejection passes. |
| OpenAPI | SDK/CI guard | export -> pinned generator -> generated diff | WIRED | Named drift test checks live operation coverage/configuration; manual advance mapping confirms current concrete link. |

### Data-Flow Trace (Level 4)

| Rendered value | Real source | Trace/result | Status |
|---|---|---|---|
| Lesson list/source/units | SQLite repositories | Query handlers -> HTTP DTO -> generated client -> TanStack Query/state -> render | FLOWING |
| Practice item/category | Accepted-unit generation, stored session, deterministic evaluator | Public commands -> practice response -> FocusPracticeMode -> registry renderer | FLOWING |
| Submitted/reference | Submit response | Prop reaches card, but submitted only incorrect/corrected; expected only after reveal | PARTIAL relative to truth 3 |
| Explanation/used/missed chunks | Evaluator/chunk_record -> persisted AttemptRow -> submit response | Full payload reaches renderer; no rendered consumer | DISCONNECTED at render |
| Resumed chunks | Persisted chunk JSON | History DTO omits fields -> resume supplies [] | HOLLOW_PROP; not merely loading defaults |
| Public module description | Validated catalog | Public allowlist query -> diagnostics router | FLOWING |
| Next practice view | Persisted session | generated practiceAdvance -> production advance handler/port -> reread -> UI | FLOWING |

### Behavioral Spot-Checks — Fresh Verifier Results

All commands used explicit repository workdir. Existing uv-managed CPython 3.14 `.venv` and installed frontend runtime were used; no installation or server startup. Each backend row is one exact named test, not a full suite. Common command prefix: `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider`; append the exact node below and `-q`.

| Exact selected test / command | Fresh outcome | Evidence boundary |
|---|---|---|
| backend/tests/adapters/http/test_openapi_client_drift.py::test_typescript_client_matches_openapi_and_ci_rejects_drift | exit 0; 1 passed in 3.40s | Current live OpenAPI export coverage and generator/CI configuration; does not execute CI or regenerate byte-for-byte output. |
| backend/tests/application/test_practice_retry.py::test_incorrect_stays_and_a_later_match_is_corrected | exit 0; 1 passed in 1.76s | Real temporary migrated persistence, capture/accept/generate/start, incorrect stays, correction, advance/finish/history. |
| backend/tests/adapters/persistence/test_compose_migrate_then_health.py::test_api_process_migrates_before_health_can_be_served | exit 0; 1 passed in 1.08s | Monkeypatched execvp; ordering only, not Docker health or restart. |
| backend/tests/modules/exercise_gap_fill/test_feedback.py::test_incorrect_explanation_matches_d18_and_records_missed | exit 0; 1 passed in 0.04s | Correct payload records missed target; does not render learner feedback. |
| backend/tests/application/test_handler_isolation.py::test_handler_isolation | exit 0; 1 passed in 1.58s | Independent application boundary assertion. |
| backend/tests/catalog/test_startup_validation.py::test_duplicate_module_id_refuses_startup | exit 0; 1 passed in 1.33s | Invalid duplicate catalog actually rejected. |
| node frontend/node_modules/vitest/vitest.mjs run --root frontend src/registries/renderers/gapFillRenderer.test.tsx -t 'shows a labeled typed answer and locks it after a grade' --reporter=verbose | exit 0; 1 passed, 5 filtered/skipped; selected test 195ms; total 24.40s | Real renderer grade/read-only behavior; assertions preserve hidden reference before reveal, not EVAL-05 completeness. |

**Environment classification:** No test-environment failure or unresolved blocker. Git initially rejected sandbox ownership; read-only commands used per-command `-c safe.directory=D:/Helsing/gitHub/LAIT`, without global configuration changes. One Windows rg wildcard path failed (os error 123); rerunning with `-g '*-PLAN.md'` on the directory succeeded. Neither is a product defect. Vitest exceeded the <10s spot-check target due harness startup; selected behavior took 195ms and passed. The five skips are selection filtering, not disabled tests.

No full suite, build, generator, live CI, Docker smoke or browser restart was run. Database writes were confined to test-owned temporary fixtures; learner data and repository implementation were not mutated.

**Valid previous evidence retained:** The prior report's retry, ordering, isolation and startup passes remain consistent with these fresh runs. Its dated drift failure `AssertionError: ['practice.advance -> practiceAdvance']` was genuine at 2026-10-06T17:32:54Z but is superseded by current code and the fresh green test; it is not a remaining gap. Prior public registry/proof and lesson persistence code evidence is retained with scoped regression inspection.

### Probe Execution

No phase-declared `probe-*.sh`, PASS-stage shell probe or conventional relevant probe was found. Step 7c not applicable; named pytest/Vitest checks above were executed, not substituted with SUMMARY claims.

### Requirements Coverage

All 17 Phase 1 IDs occur in PLAN requirements; no orphaned Phase 1 requirements or extra plan IDs. Requirement documents were not changed.

| Requirement | Source plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| LESS-01 | 01-01,06,14 | Paste English without account/language selection | SATISFIED in code | lessonCreate, source form and real handler/persistence |
| LESS-02 | 01-01,06 | List/open active lessons | SATISFIED in code | list/get queries and /lessons/:id; restart acceptance pending |
| ANLY-08 | 01-03,06,14 | Manual source-linked units | SATISFIED | add/accept commands exercised in retry setup |
| EXER-01 | 01-05,06,14 | Accepted-only generation and recoverable status | SATISFIED | Accepted-unit generation handler, persisted terminal status |
| EXER-02 | 01-05,07,12,13 | One item at a time | SATISFIED | Current cursor/item mapping and named retry/advance behavior |
| EXER-03 | 01-04,07,15,16 | Registry Gap Fill practice | SATISFIED | Registry renderer, real generate/submit loop |
| EXER-07 | 01-05,07,11,13 | Submit, feedback, Continue in session | SATISFIED for basic flow | Same-session category and generated Continue work; required detailed content is separately blocked under EVAL-05 |
| EVAL-01 | 01-04,07 | Deterministic grading | SATISFIED | Module evaluator before any model; retry/payload tests |
| EVAL-04 | 01-04,07 | Explicit categories | SATISFIED with retained specification note | correct/incorrect/corrected explicit; corrected extends original five-category vocabulary, not a newly raised blocker |
| EVAL-05 | 01-04,07,15,16 | Answer/reference/explanation/chunks/optional alternative | BLOCKED | Required fields not visible in session; history loses chunks |
| MODL-01 | 01-02 | Validate and reject invalid catalogs | SATISFIED | Startup gate plus passing duplicate-ID rejection |
| MODL-02 | 01-02 | Public active-module inspection | SATISFIED | Allowlisted module_registry.describe |
| MODL-03 | 01-02,04,07,09 | Proof via public seams | SATISFIED, regression scope | Contribution and renderer registration; no core private-module dependency observed |
| MODL-12 | 01-01,08,09 | Public commands/queries, no table access | SATISFIED | Handler/router seam and named isolation pass |
| PLAT-03 | 01-09,10 | Compose migration then health | NEEDS HUMAN — WARNING | Process-ordering test passes; actual Compose phase smoke unproven |
| PLAT-09 | 01-08 | Generated TS client and mismatch gate | SATISFIED in current workspace | Named drift pass plus actual practiceAdvance types/export/use and CI diff configuration |
| PLAT-10 | 01-09 | Independent core/persistence/modules tests | SATISFIED | Separate CI paths and successful selected application, persistence and module commands |

### Anti-Patterns and Test Quality

| Location | Finding | Severity | Disposition |
|---|---|---|---|
| GapFillRenderer.tsx:172-190 | Required feedback fields omitted | BLOCKER | Carried-forward must-have gap; no override |
| LessonWorkspacePage.tsx:201-202 | Resume chunk arrays hardcoded empty | BLOCKER detail | Same feedback root cause; stored data cannot flow through current history DTO |
| Phase implementation/test/config paths scanned | No unresolved TBD/FIXME/XXX or disabled-test markers found | None | Null guards/loading defaults are not stubs |
| GapFillRenderer.tsx:26-32 | WR-01 Try again readOnly warning | WARNING, historical | Prior review/disposition remains open; not freshly reproduced or promoted to blocker |
| repositories.py:419-425 | WR-02 overlapping-submit cursor/concurrency warning | WARNING, historical | Not part of carried-forward gap closure; no fresh red evidence |
| test_openapi_client_drift.py | WR-03 verb/path checks are not bound to each export | WARNING | Green coverage test is not exhaustive schema equivalence; concrete advance binding manually verified |

No new unevidenced blocker is introduced under the re-verification evidence gate. Selected tests use explicit state/value assertions, not self-fulfilling circular oracles. Test temporary fixtures supply normal production inputs, not missing production preconditions. Handler isolation is a boundary check, not an end-to-end runtime proof. The renderer and payload tests are intentionally insufficient to certify the missing learner-visible EVAL-05 content. No skipped-test debt was inferred from Vitest name filtering.

### Decision Coverage, Prohibitions and Backstop Abstentions

Official decision-coverage query returned 23/23 for 01-CONTEXT.md, no not_honored items; this is an advisory artifact comparison, not a behavioral oracle. The prior 01-14-CONTEXT parsing limitation is retained as non-blocking.

PLAN prohibitions are string-form judgment constraints, not wired deterministic negative tests. Code inspection provides **NON-AUTHORITATIVE** evidence only: public catalog output excludes private details, learner pages avoid module_registry.describe, generated client has no observed provider/environment secrets, browser grades come from response, proof is excluded by learner visibility, fonts are local, core/application boundaries remain, and corrected required no new migration. The former handwritten advance transport is now removed from the feature. These observations do not silently grant human approval to all prohibitions.

**unverified-prohibition — human review recommended.** Plan-local no-edit/no-regenerate/label/layout constraints and visual prohibitions remain UNCERTAIN (WARNING) absent explicit human resolution or wired enforcement. Scope of these constraints is each owning plan, not a blanket ban on later approved plans changing earlier implementation. No purported test-tier prohibition was marked green without enforcement. Required human decisions are preserved even though the overall status is gaps_found.

Prior backstop abstentions remain **UNCERTAIN (WARNING), insufficient_spec**, not verified by presence and not included in the frozen five-truth score: overlapping SQLite create/list with busy_timeout, concurrent catalog handlers, concurrent/double submit, title truncation/overflow, 320px sentence wrapping, interrupted generator and restart/persistence user flows. No held-out/property test or direct behavior observation was supplied this pass. Human decisions are still needed; a green named retry test does not prove concurrency.

### Human Verification Required

These items remain required even though the overall status is gaps_found. No `human-check` blocks were found to harvest from the phase plans.

#### 1. Required phase-level Docker learner-flow smoke

**Test:** On the actual Docker app at http://127.0.0.1:5173, keep the volume; paste a lesson, capture and accept a unit, generate Gap Fill, submit an incorrect then corrected answer, continue and finish. Reopen via list, reload, navigate directly, restart the actual browser process, and restart Docker/app without deleting the volume. Separately establish fresh-volume migration/health readiness if no recorded acceptance exists.
**Expected:** Healthy only after migrations; durable source/units/generation/session state through applicable paths; EVAL-05 satisfies the approved compact-card/Details disclosure and full saved-content contract, with no reduced-content override.
**Why human:** Governance requires phase-level smoke before phase.complete; the process test substitutes execvp and plan approvals do not replace this gate. No fresh Compose, actual browser-process restart or completed phase smoke record was observed. The smoke result must be recorded in 01-VALIDATION.md by the authorized workflow, not by this report-only verifier.

#### 2. Feedback contract decision — resolved; behavior approval pending

**Decision:** The user approved compact feedback with expandable Details on 2026-10-07; D-24–D-31 retain the full EVAL-05 educational payload and control disclosure timing. No further reduced-content decision or verification override is required.
**Pending test:** Execute the final blocking-human task of 01-18 on Docker, including hidden/revealed/correct/corrected restoration across all required entry/restart routes with volume kept.
**Expected:** The implemented card and complete restored payload agree with the approved contract. Stored data alone does not count as accessible educational feedback; Details alone never discloses an incorrect solution.
**Why human:** Specification approval is not implementation approval. Automatic checks and historical 01-15/16 approvals cannot close the new 01-18 checkpoint.

#### 3. Remaining judgment and non-inferable checks

**Test:** Resolve applicable PLAN prohibitions individually; inspect layout/fonts/long source and 320px wrapping; provide explicit behavior evidence or a human decision for the backstop concurrency, overflow, interrupted-generation and restart invariants above.
**Expected:** No forbidden effect within each plan's scope; no hidden concurrency corruption, overflow or partial-generation publication; user-visible error/recovery states are understandable.
**Why human:** No wired negative enforcement/held-out tests or current visual/runtime observations establish these assertions. Historical review notes and code presence are insufficient.

### Gaps Summary and Terminal Routing

One **BLOCKER** remains: the current learner-visible feedback is narrower than EVAL-05 and the roadmap, including loss of chunk details on resume. The generated-client gap is closed in the current workspace. No remaining gap is specifically deferred by a later roadmap phase.

Truth 1 remains **PRESENT_BEHAVIOR_UNVERIFIED**, so closing the feedback gap alone would still leave human_needed until required manual evidence is supplied. Plan 01-15/16 approvals do not authorize phase completion. G-01-1 is resolved and is not reopened.

Planning amendment: gap plans 01-17 → 01-18 are prepared and independently checked; see 01-17-PLAN-CHECK.md. Execution is not authorized by this planning-only request. Only a later explicit execution request may start them; required Docker checkpoint, phase learner smoke and re-verification remain pending before phase completion.

---

_Verified: 2026-10-06T20:52:32Z_
_Verifier: Codex (gsd-verifier)_
