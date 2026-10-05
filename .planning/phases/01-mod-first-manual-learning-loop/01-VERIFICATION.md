---
phase: 01-mod-first-manual-learning-loop
verified: 2026-10-02T03:00:01Z
status: human_needed
score: 4/5 must-haves verified
behavior_unverified: 1
overrides_applied: 0
nyquist_compliant: false
decision_coverage:
  honored: 23
  total: 23
  not_honored: []
covered_files:
  - .dockerignore
  - .env.example
  - .github/workflows/ci.yml
  - .gitignore
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
  - .planning/WINDOWS.md
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
  - .planning/phases/01-mod-first-manual-learning-loop/01-REVIEW-DISPOSITION.md
  - .planning/phases/01-mod-first-manual-learning-loop/01-REVIEW.md
  - .planning/phases/01-mod-first-manual-learning-loop/deferred-items.md
  - .python-version
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
  - backend/lait/application/commands/practice_finish.py
  - backend/lait/application/commands/practice_start.py
  - backend/lait/application/commands/practice_start_over.py
  - backend/lait/application/commands/unit_set_freeze.py
  - backend/lait/application/ports.py
  - backend/lait/application/queries/__init__.py
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
  - backend/tests/adapters/http/test_openapi_contract.py
  - backend/tests/adapters/persistence/test_lesson_repository.py
  - backend/tests/adapters/persistence/test_one_open_practice_session.py
  - backend/tests/application/test_exercise_generate.py
  - backend/tests/application/test_handler_isolation.py
  - backend/tests/application/test_learning_unit_accept.py
  - backend/tests/application/test_learning_unit_add.py
  - backend/tests/application/test_learning_unit_remove.py
  - backend/tests/application/test_lesson_create.py
  - backend/tests/application/test_lesson_list.py
  - backend/tests/application/test_practice_finish_and_start_over.py
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
  - frontend/src/registries/renderers/types.ts
  - frontend/src/styles/tokens.css
  - frontend/src/vite-env.d.ts
  - frontend/tsconfig.app.json
  - frontend/tsconfig.json
  - frontend/vite.config.ts
  - pyproject.toml
  - tsconfig.json
  - uv.lock
covered_digest: "v2:sha256:e91b69862eae905179b295a879b25dc03aabaf086261035826dbd675365b24af"
re_verification:
  previous_status: gaps_found
  previous_score: 3/5
  gaps_closed:
    - "Learner can manually add and accept a source-linked learning unit, generate a Gap Fill exercise from it, and complete the exercise one item at a time. A refresh or a second Start Practice no longer leaves an open row the UI cannot finish."
  gaps_remaining: []
  regressions: []
behavior_unverified_items:
  - truth: "Learner can start the health-checked application with Docker Compose, paste English text into a lesson, and reopen that lesson from the local lesson list."
    test: "docker compose up -d --wait on a fresh volume, then paste a lesson and reopen it from /."
    expected: "API becomes healthy only after Alembic upgrade head, and the pasted lesson is listed and reopenable."
    why_human: "Entrypoint orders migrate() before uvicorn, and the healthcheck calls /health, but no test executes Compose. Paste and reopen stay covered by handler tests; the live health ordering was not run."
human_verification:
  - test: "docker compose up -d --wait on a fresh volume, then paste a lesson and reopen it from /."
    expected: "Healthy only after migrations. Lesson appears on / and opens at /lessons/:id."
    why_human: "No probe runs Compose. This pass did not start containers."
---

# Phase 1: Mod-First Manual Learning Loop Verification Report

**Phase Goal:** A learner can launch the local application and complete a source-to-feedback Gap Fill workflow, while maintainers can observe that it runs through documented public contracts.
**Verified:** 2026-10-02T03:00:01Z
**Status:** human_needed
**Re-verification:** Yes — after gap closure

Roadmap marks this phase `mode: mvp`, but the goal is not a user story (`As a …, I want to …, so that …`). Verification used the five roadmap success criteria as the contract. Plan `must_haves` were checked against the code and folded into those criteria when they restated them. `nyquist_compliant` stays false. Closure is plan 01-12 and commit `bde7eca` (`fix: resolve post-merge conflicts from wave 7`) on `phase/01-execution`. `main` is still `6d00e33be532e8137c46e1f995f6ebcc61a74058`. Phase completion, ROADMAP, STATE, and REQUIREMENTS were not edited.

`01-12-SUMMARY.md` still says the unique-index test lives in `backend/tests/application/test_practice_start.py`. The code after `bde7eca` does not. The index check is `backend/tests/adapters/persistence/test_one_open_practice_session.py`. The winner id is `test_start_returns_the_session_the_port_stored`, a port fake. Those files were read and the named tests were run.

## User Flow Coverage

User story form is absent. Steps below are the roadmap success criteria as learner and maintainer outcomes.

| Step | Expected | Evidence | Status |
|------|----------|----------|--------|
| Start the local app | Compose migrates, then `/health` can pass | `docker/api_entrypoint.py` calls `migrate()` then `execvp` uvicorn. `docker-compose.yml` healthcheck opens `/health` and web waits on `service_healthy`. | ⚠️ present, Compose not executed |
| Paste and reopen a lesson | English paste creates a lesson; `/` lists it; `/lessons/:id` reopens it | `App.tsx` routes `/` and `/lessons/:id`. `lesson.create` / `lesson.list` / `lesson.get` still present. | ✓ regression |
| Add, accept, generate, finish one item | Source span becomes an accepted unit, Gap Fill is generated, one current item is completed, and a refresh or second start can still finish | `practice.start` returns the open session when the snapshot matches. Mismatch raises `StaleGenerationError` and does not unfreeze. Workspace restores `lait.practice-session.{lessonId}` through `practice.get`. Named pytest and vitest tests passed. | ✓ |
| See feedback and continue | Card shows answer, reference, used/missed, explanation, optional alternative, Continue | `evaluate()` still returns `correct`/`incorrect` and `natural_alternative=None`. Prior named submit and Focus Practice tests were not re-run; symbols and wiring remain. | ✓ regression |
| Inspect contracts and proof seam | describe, commands/queries, proof registry/renderer, startup reject | `create_app` still calls `validate_catalog` before `include_routers`. No new operation id. Decision coverage 23/23. | ✓ regression |
| Client, CI drift, independent tests | Generated TS client, dirty-diff gate, split pytest paths | `lessonApi.ts` still imports the generated client. CI still splits persistence and application pytest and diffs `frontend/src/api/generated`. `test_handler_isolation` passed. | ✓ |

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | ------- | ---------- | ---------- |
| 1 | Learner can start the health-checked application with Docker Compose, paste English text into a lesson, and reopen that lesson from the local lesson list. | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Lesson routes and create/list handlers are still present. Compose health-after-migrate is code-ordered (`migrate` then uvicorn) and was not run. |
| 2 | Learner can manually add and accept a source-linked learning unit, generate a Gap Fill exercise from it, and complete the exercise one item at a time. | ✓ VERIFIED | Same-generation `practice.start` returns the stored open session. A rewritten snapshot raises `StaleGenerationError`, leaves that row open, and `learning_unit.accept` still raises `UnitSetFrozenError`. Refresh calls `practice.get` for `lait.practice-session.{lessonId}`, shows the frozen hint while pending, then Exit Practice. Start Practice stays disabled until the request settles. Tests below passed. |
| 3 | Learner receives deterministic result-category feedback containing their answer, the reference, target chunks used or missed, a concise explanation, an optional natural alternative, and the next-exercise action without leaving the session. | ✓ VERIFIED | Regression: `evaluate.py` still sets `correct`/`incorrect` and `natural_alternative=None`. Submit and Focus Practice wiring from the prior pass was not re-executed. |
| 4 | Maintainer can inspect active modules and capabilities, invoke the workflow through documented commands and queries, add a proof exercise contribution through the public registry and renderer seams without changing core domain services, and see startup reject invalid or incompatible module catalogs. | ✓ VERIFIED | Regression: `validate_catalog` still runs before routers. Practice router operation ids are unchanged (`practice.start`, `practice.get`, `exercise.submit_attempt`, `practice.finish`, `practice.start_over`). Decision coverage 23/23. |
| 5 | Maintainer can generate the TypeScript client from OpenAPI, have CI detect an unreviewed contract/client mismatch, and test the core, persistence adapter, and bundled modules independently. | ✓ VERIFIED | Regression: CI still has the split pytest commands and `git diff --exit-code -- frontend/src/api/generated`. `test_handler_isolation` passed on this pass. |

**Score:** 4/5 truths verified (1 present, behavior-unverified)

### Advisory (New Scope, Unevidenced)

None. The prior open-session deadlock was the carried-forward gap and is closed in code. No new Step 7 blocker was raised on files this closure edited.

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | ----------- | ------ | ------- |
| `docker-compose.yml` | Migrate-then-health stack | ✓ VERIFIED | API healthcheck on `/health`; web `depends_on` healthy. Live Compose not run. |
| `docker/api_entrypoint.py` | Alembic before listen | ✓ VERIFIED | `migrate(database_url)` then `os.execvp` uvicorn. |
| `frontend/src/app/App.tsx` | Lesson list and workspace routes | ✓ VERIFIED | `/` and `/lessons/:id`. |
| `backend/lait/application/commands/practice_start.py` | Return the same-generation open session | ✓ VERIFIED | Matching snapshot returns `view_for`. Mismatch raises `StaleGenerationError`. No unfreeze call. |
| `backend/lait/adapters/persistence/repositories.py` | One-transaction insert | ✓ VERIFIED | `insert_open_practice_session` selects the open row and inserts in one session. `IntegrityError` rolls back and re-reads the winner. |
| `backend/alembic/versions/20261002_0004_one_open_practice_session.py` | Partial unique index | ✓ VERIFIED | `down_revision = 20261001_0003`. Creates `uq_practice_sessions_one_open_per_lesson` on `lesson_id` WHERE `status = 'open'`. |
| `backend/lait/adapters/persistence/models.py` | Same index on the model | ✓ VERIFIED | `sqlite_where` and `postgresql_where` both `status = 'open'`. `lesson_id` index kept. |
| `frontend/src/features/lesson/stageState.ts` | Per-lesson session id | ✓ VERIFIED | Key `lait.practice-session.${lessonId}`. `isPracticeOpen(pendingStoredSession, sessionOpen)` has no `focused` parameter. |
| `frontend/src/features/lesson/LessonWorkspacePage.tsx` | Restore into Focus Practice | ✓ VERIFIED | Load reads the key, calls `getPractice`, keeps `pendingStoredSession` true until settle, passes `isPracticeOpen(...)`. Exit calls `finishPractice` and clears the key. |
| `frontend/src/features/lesson/stages/PracticeStage.tsx` | In-flight disable | ✓ VERIFIED | `disabled={!enabled \|\| pending}`. `handleStart` sets a ref before await and clears it in `finally`. |
| `frontend/src/registries/renderers/registry.ts` | exercise_type registry | ✓ VERIFIED | Unchanged regression: gap-fill and proof registration from the prior pass. |
| `.github/workflows/ci.yml` | Drift gate and split tests | ✓ VERIFIED | Dirty diff on `frontend/src/api/generated`; separate pytest path steps. |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| Create Lesson | `lesson.create` | generated client | WIRED | `lessonApi.ts` still calls `lessonCreate`. |
| `LessonWorkspacePage` load | `practice.get` | `lait.practice-session.{lessonId}` | WIRED | Effect calls `getPractice(sessionId)`. Open view sets `session` and `focused`. Closed or failed get clears the key. Load does not call `practice.start` or `practice.finish`. |
| `LessonWorkspacePage` | `LearningUnitsStage` `practiceOpen` | `isPracticeOpen(pendingStoredSession, session?.open === true)` | WIRED | `focused` is not an argument. Pending stored id forces the frozen hint before Focus Practice replaces the stage column. |
| `practice.start` | `insert_open_practice_session` | one transaction; return existing row when the snapshot matches | WIRED | Port method on `LearningUnitRepository`, `SqlAlchemyPracticeRepository`, `SqlAlchemyLearningUnitRepository`, and `RepositoryBundle`. Handler returns `view_for` of the stored session. |
| `PracticeSessionRow` | `uq_practice_sessions_one_open_per_lesson` | Alembic `20261002_0004` after `20261001_0003` | WIRED | Model index and migration both create the partial unique index. Persistence test rejects a second open insert. |
| `PracticeStage` | `handleStart` | pending flag cleared in `finally` | WIRED | Second click while the ref is set does not call `startPractice` again. Button is disabled for the whole request, including a rejected request. |
| Submit Answer | `exercise.submit_attempt` | API | WIRED | Regression: client still sends the current item. |
| `create_app` | catalog validation | raise before serve | WIRED | `validate_catalog` then `include_routers`. |
| OpenAPI export | generated client | `openapi:generate` + CI diff | WIRED | Workflow steps still fail on a dirty generated tree. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `LessonListPage` | lessons | `lesson.list` query | Yes, repository list | ✓ FLOWING |
| `LessonWorkspacePage` | source, units | `lesson.get`, `learning_unit.list` | Yes | ✓ FLOWING |
| `LessonWorkspacePage` | open session id | `localStorage` then `practice.get` | Yes, when the stored view is open | ✓ FLOWING |
| `LearningUnitsStage` | frozen hint | `isPracticeOpen(pendingStoredSession, session.open)` | Pending stored id or `session.open` | ✓ FLOWING |
| `GapFillRenderer` | item segments, feedback | `practice.get` / `exercise.submit_attempt` | Yes, after resume or start | ✓ FLOWING |
| `FeedbackStage` | attempts | React `attempts` state | Server rows are not reloaded | ⚠️ HOLLOW after reload |
| `module_registry.describe` | public module rows | validated in-memory catalog | Yes | ✓ FLOWING |

`FeedbackStage` attempt history still lives in component state. That was not the failed truth. Resume restores the open session and Exit Practice; it does not replay stored attempts into the feedback list.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Second start returns the same open session and stays frozen | `pytest …::test_second_start_returns_the_same_open_session` | passed | ✓ PASS |
| Generate again keeps that open session | `pytest …::test_generate_again_keeps_the_open_session_for_the_next_start` | passed | ✓ PASS |
| Snapshot mismatch stays open and frozen | `pytest …::test_open_session_snapshot_mismatch_stays_open_and_frozen` | passed | ✓ PASS |
| Winner id comes from the port, not the minted id | `pytest …::test_start_returns_the_session_the_port_stored` | passed | ✓ PASS |
| Partial unique index rejects a second open row | `pytest …::test_partial_unique_index_rejects_a_second_open_row` | passed | ✓ PASS |
| Insert returns the existing open row | `pytest …::test_insert_open_practice_session_returns_the_existing_open_row` | passed | ✓ PASS |
| Application tests do not import SQLAlchemy or persistence models | `pytest …::test_handler_isolation` | passed | ✓ PASS |
| Start over still abandons and leaves units frozen | `pytest …::test_start_over_keeps_attempts_and_leaves_units_frozen` | passed | ✓ PASS |
| Finish still closes and unfreezes | `pytest …::test_finish_closes_session_and_unfreezes_units` | passed | ✓ PASS |
| Stored id resumes Focus Practice after the frozen hint | `vitest run LessonWorkspacePage.test.tsx PracticeStage.test.tsx` | 17 passed | ✓ PASS |
| Compose health after migrate | not run | no container started | ? SKIP |

The 14 pytest cases above passed in one invocation (3.43s), including the older practice-start cases in the same file. Vitest on `LessonWorkspacePage.test.tsx` and `PracticeStage.test.tsx` passed 17 tests (3.66s). The orchestrator count of 93 pytest passes was not re-run and is not treated as evidence. `01-12-SUMMARY.md` test locations were checked against the files, not accepted from the summary.

### Probe Execution

No `scripts/*/tests/probe-*.sh` declarations in the phase plans. Step 7c skipped.

### Requirements Coverage

Every Phase 1 id in `REQUIREMENTS.md` appears in at least one plan `requirements:` list. No Phase 1 id is orphaned. No plan id falls outside this set. Checkboxes in `REQUIREMENTS.md` were not edited.

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| LESS-01 | 01-01, 01-06 | Paste English with no account or language | ✓ SATISFIED | Create handler and routes still present |
| LESS-02 | 01-01, 01-06 | List and open active lessons | ✓ SATISFIED | `/` and `/lessons/:id` |
| ANLY-08 | 01-03, 01-06 | Manual source-linked unit | ✓ SATISFIED | `learning_unit.add` still on the router |
| EXER-01 | 01-05, 01-06 | Generate only from accepted units with terminal status | ✓ SATISFIED | Regression from the prior pass |
| EXER-02 | 01-05, 01-06, 01-12 | Start a session and receive one exercise at a time | ✓ SATISFIED | Same-generation return, unique open row, localStorage resume, in-flight disable. Named tests passed. |
| EXER-03 | 01-04, 01-07 | Complete Gap Fill from the exercise registry | ✓ SATISFIED | Regression |
| EXER-07 | 01-05, 01-07, 01-11 | Submit, see feedback, continue without leaving the session | ✓ SATISFIED | Regression. Exit Practice remains `practice.finish`. |
| EVAL-01 | 01-04, 01-07 | Deterministic closed-answer grading | ✓ SATISFIED | `evaluate.py` still grades to two categories |
| EVAL-04 | 01-04, 01-07 | Explicit result category | ✓ SATISFIED | `correct` or `incorrect` |
| EVAL-05 | 01-04, 01-07 | Submitted, reference, explanation, chunks, optional alternative | ✓ SATISFIED | Evaluation fields unchanged |
| MODL-01 | 01-02 | Refuse invalid catalogs | ✓ SATISFIED | `validate_catalog` before routers |
| MODL-02 | 01-02 | Inspect active modules without private details | ✓ SATISFIED | `module_registry.describe` still the operation id |
| MODL-03 | 01-02, 01-04, 01-07, 01-09 | Add proof through public seams | ✓ SATISFIED | Regression |
| MODL-12 | 01-01, 01-08, 01-09 | Commands/queries, no direct table access from callers | ✓ SATISFIED | `test_handler_isolation` passed. Application tests do not import `sqlalchemy` or `lait.adapters.persistence.models`. |
| PLAT-03 | 01-10, 01-09 | Compose migrate then healthy | ? NEEDS HUMAN | Entrypoint and healthcheck exist; Compose was not executed |
| PLAT-09 | 01-08 | OpenAPI TypeScript client and CI mismatch detection | ✓ SATISFIED | Generated client import and CI diff step |
| PLAT-10 | 01-09 | Test core, persistence, and modules independently | ✓ SATISFIED | CI path split. Unique-index test is in the persistence suite. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| Closure files (`practice_start.py`, `repositories.py`, `stageState.ts`, `LessonWorkspacePage.tsx`, `PracticeStage.tsx`, migration `20261002_0004`) | — | `TBD` / `FIXME` / `XXX` | none | No debt markers. |

Prior review warnings (untargeted submit, cursor overwrite, selection offsets, overlap error copy, overlap check vs insert, broad generate `except`, blank last Continue, list error copy) were not part of the carried-forward gap and were not re-promoted.

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `backend/tests/application/test_practice_start.py` | EXER-02 | 9, including same-session return, generate-again, mismatch freeze, port-fake winner id | 0 | no | Behavioral | PASS |
| `backend/tests/adapters/persistence/test_one_open_practice_session.py` | EXER-02 | 2, index name plus one open row, insert returns the existing id | 0 | no | Value | PASS |
| `backend/tests/application/test_handler_isolation.py` | MODL-12, PLAT-10 | AST ban on `sqlalchemy` and `lait.adapters.persistence.models` in application code and application tests | 0 | no | Behavioral | PASS |
| `frontend/src/features/lesson/LessonWorkspacePage.test.tsx` | EXER-02 | resume after frozen hint, `isPracticeOpen` arity 2, clear closed session, disable until settle, re-enable after reject | 0 | no | Behavioral | PASS |
| `frontend/src/features/lesson/stages/PracticeStage.test.tsx` | EXER-02 | pending disables the button; disabled stays disabled | 0 | no | Behavioral | PASS |

**Disabled tests on requirements:** 0
**Circular patterns detected:** 0
**Insufficient assertions:** 0

`test_start_returns_the_session_the_port_stored` asserts `view.session_id == "winner-open"` while the minted id is `"minted-id"`. It does not import SQLAlchemy. The unique-index `IntegrityError` is asserted in the persistence test with `sqlite3.IntegrityError`, not in the application suite.

### Decision Coverage

All trackable CONTEXT.md decisions are honored by shipped artifacts (23/23). Non-blocking.

### Prohibitions

Judgment-tier prohibitions from plan 01-12 were checked in source. This is a non-authoritative review.

- No new command, query, or HTTP route. Practice operation ids are unchanged.
- `practice_start.py` does not unfreeze. The mismatch test still sees `UnitSetFrozenError`.
- `practice_start_over.py` still calls `practice.start` after abandon. `test_start_over_keeps_attempts_and_leaves_units_frozen` passed. `bde7eca` did not edit that module.
- Start Over is not in the router.
- The unique index is an Alembic revision. No SQLite file was hand-edited.
- `isPracticeOpen` does not take `focused`. The workspace does not pass `focused` as `practiceOpen`.

**unverified-prohibition — human review recommended** for visual prohibitions carried from the prior pass (320px wrap, title truncation, self-hosted font rendering). Those remain `verification: backstop` and were not executed in a browser.

### Backstop Abstentions

These plan truths are `verification: backstop`. They are not scored and do not add another gap:

- SQLite `busy_timeout` under overlapping create/list.
- Catalog validation observed once by concurrent handlers.
- Concurrent double-submit serialization.
- Title truncation, two-line create field, 320px source and Gap Fill wrap.
- Interrupted `openapi:generate` leaves a dirty tree.
- An empty independent suite directory fails CI. `test_handler_isolation` does run an empty pytest directory and asserts a non-zero exit; that one backstop now has a test. The others were not executed.
- Cross-suite pytest order is not relied on.

### Human Verification Required

### 1. Compose health

**Test:** `docker compose up -d --wait` on a fresh volume, then paste a lesson and reopen it.
**Expected:** Healthy only after migrations. Lesson appears on `/` and opens at `/lessons/:id`.
**Why human:** No probe runs Compose. This pass did not start containers.

The previous stranded-session check is closed by code and tests: a stored open id resumes Focus Practice after the frozen hint, and a second start returns that session when the accepted-set snapshot matches.

### Gaps Summary

The carried-forward gap is closed. `practice.start` returns the existing open session when that session's accepted-set snapshot matches the current accepted ids, and raises `StaleGenerationError` on a mismatch without closing the row or unfreezing units. `uq_practice_sessions_one_open_per_lesson` rejects a second open row. Workspace load reads `lait.practice-session.{lessonId}`, calls `practice.get`, and while that call is pending keeps `practiceOpen` true through `isPracticeOpen`. `focused` is not an input. Start Practice stays disabled until the request settles. `test_handler_isolation` passed.

The phase is not marked complete. Truth 1 stays present and behavior-unverified because Compose was not run. Status is `human_needed`. Score is 4/5.

---

_Verified: 2026-10-02T03:00:01Z_
_Verifier: Claude (gsd-verifier)_
