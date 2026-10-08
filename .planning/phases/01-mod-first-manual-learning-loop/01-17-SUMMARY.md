---
phase: 01-mod-first-manual-learning-loop
plan: 17
subsystem: api
tags: [saved-feedback, sqlite, attempt-query, openapi, tdd]
requires:
  - phase: 01-16
    provides: "Persisted attempts, same-session retry rounds, corrected semantics and opening-pass denominator"
provides:
  - "Complete saved feedback through reopened SQLite, domain, application query, HTTP and generated client"
  - "Exact saved attempt id and learning-unit id with strict persisted chunk-array validation"
  - "Independent rich/empty/legacy feedback and frozen progression regression evidence"
affects: [01-18, EVAL-05]
actuals:
  tokens: 10494
  tasks: 2
  commits: 0
plan_head_before: a2220b13a4abf4d7986df08a915b380a39f4782b
plan_head_after: a2220b13a4abf4d7986df08a915b380a39f4782b
tech-stack:
  added: []
  patterns:
    - "Required saved educational fields at each projection; no synthetic empty defaults"
    - "Decode persisted JSON string arrays to tuples; explicit HTTP tuple-to-list conversion"
key-files:
  created:
    - .planning/phases/01-mod-first-manual-learning-loop/01-17-SUMMARY.md
  modified:
    - backend/lait/domain/practice_session.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/application/queries/attempt_list_for_lesson.py
    - backend/lait/adapters/http/routers/practice.py
    - backend/tests/adapters/http/test_http_dto_mapping.py
    - backend/tests/adapters/persistence/test_lesson_reopen_reads.py
    - backend/tests/application/test_lesson_reopen_reads.py
    - frontend/openapi.json
    - frontend/src/api/generated/types.gen.ts
key-decisions:
  - "Original saved explanation, submitted answer, expected answer, chunk arrays and nullable alternative remain authoritative."
  - "Malformed saved chunk JSON or non-string arrays fail reads rather than becoming empty feedback."
  - "Stored learning-unit identity is exposed without inventing an attempt position or assigning a retry copy."
  - "Only 01-17 is executed; parent owns shared state updates and dispatches 01-18."
patterns-established:
  - "Saved feedback reads carry the same educational payload as live submit responses."
requirements-completed: []
requirements-addressed: [EVAL-05]
requirement-closure: "01-17 saved-data tasks are complete. D-32–D-37 explicitly narrow Phase 1; original full EVAL-05 stays partial with teaching/chunk/alternative UI deferred to Phase 5. 01-18 R2 checkpoint approved 2026-10-07; separate phase smoke/re-verification pending."
coverage:
  - id: D1
    description: "Fresh SQLite-to-HTTP reads retain rich and empty feedback, exact identity and original legacy/raw text."
    requirement: EVAL-05
    verification:
      - kind: integration
        ref: "backend/tests/adapters/http/test_http_dto_mapping.py#test_reopened_http_lists_complete_saved_feedback_without_mutation"
        status: pass
      - kind: integration
        ref: "backend/tests/adapters/http/test_http_dto_mapping.py#test_http_maps_generate_start_get_and_submit_only"
        status: pass
    human_judgment: false
  - id: D2
    description: "Repository and application projections preserve real saved arrays, nullability, order and denominator; malformed arrays are rejected."
    requirement: EVAL-05
    verification:
      - kind: integration
        ref: "backend/tests/adapters/persistence/test_lesson_reopen_reads.py#test_reopened_repository_preserves_complete_feedback_records"
        status: pass
      - kind: integration
        ref: "backend/tests/adapters/persistence/test_lesson_reopen_reads.py#test_reopened_repository_rejects_malformed_saved_chunks"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_lesson_reopen_reads.py#test_query_forwards_complete_saved_feedback_without_mutating_records"
        status: pass
      - kind: integration
        ref: "backend/tests/application/test_practice_retry.py"
        status: pass
      - kind: integration
        ref: "backend/tests/application/test_practice_finish_and_start_over.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "Generated attempt DTO requires every saved field while existing operation bindings are retained."
    requirement: EVAL-05
    verification:
      - kind: other
        ref: "generated_attempt_dto_requires_complete_saved_feedback (exact Node command under Verification)"
        status: pass
      - kind: other
        ref: "npm --prefix frontend run typecheck"
        status: pass
      - kind: integration
        ref: "backend/tests/adapters/http/test_openapi_client_drift.py#test_typescript_client_matches_openapi_and_ci_rejects_drift"
        status: pass
    human_judgment: false
duration: 11 min
started: 2026-10-07T00:10:14.678Z
completed: 2026-10-07
completed_at: 2026-10-07T00:20:42.757Z
status: complete
---

# Phase 01 Plan 17: Complete Saved Feedback Read Path Summary

Saved attempt chunks, nullable natural alternatives, legacy explanations and exact learning-unit identity now survive reopened SQLite reads through the public query, HTTP response and generated TypeScript DTO.

This completes only the two automatic backend tasks of 01-17. EVAL-05 and Phase 1 remain open. Scope-status amendment after the user's unapproved 01-18 checkpoint (D-32–D-37): metadata now records EVAL-05 as addressed, not completed; the original full educational requirement is partially delivered with remaining teaching/chunk/alternative UI deferred. All backend implementation and evidence below are retained. No global requirement checkbox or phase-completion status is closed by this summary.

## Performance and scope

- Started: 2026-10-07T00:10:14.678Z; completed: 2026-10-07T00:20:42.757Z; duration: 11 min.
- Tasks: 2/2.
- Changed implementation/test/schema files: 9; summary artifact: 1; total owned final deliverable files: 10.
- Added pytest invocations: 15 (one HTTP, one direct repository, twelve malformed-array cases, one query).
- Commits: **0**, measured with `git rev-list --count a2220b13a4abf4d7986df08a915b380a39f4782b..HEAD`. HEAD stayed `a2220b13a4abf4d7986df08a915b380a39f4782b`.
- Local RED evidence is retained in ignored `tmp/gsd-01-17-evidence/t1-red.json` and `t2-red.json`; the durable evidence facts and reproduction commands are also recorded below.
- Actual tokens are chars/4 over the 21829-character realized nine-file diff relative to the captured dirty baseline plus this new summary. Line-ending-only differences were ignored. This is a diff-size estimate, not a model/harness token count. Pre-existing edits were excluded.

## Accomplishments

1. `AttemptRecord`, `ListedAttempt` and `AttemptListItemResponse` now require `chunks_used`, `chunks_missed`, nullable `natural_alternative` and stored `learning_unit_id`.
2. The repository decodes saved chunk arrays, checks that the decoded value is a list of strings, preserves order/duplicates/Unicode, and returns tuples. Invalid JSON, JSON null, objects, strings and arrays containing numbers/null are rejected without rewriting the row.
3. The HTTP fixture builds a real lesson, accepted unit, generation and session through production endpoints, seeds rich/null feedback through the public `add_attempt` port, and opens a fresh app/repository/TestClient against the same migrated SQLite file. Exact content, ids, order, 404 behavior and repeated read stability are asserted.
4. Independent repository and Protocol-fake query tests prove the full payload, original legacy copy, real empty arrays/null and opening denominator. Database snapshots assert that reads leave attempts, sessions, cursors and pass items unchanged.
5. Exporter and pinned generator updated only `AttemptListItemResponse` in the OpenAPI schema and the corresponding generated TypeScript type.

## Files created/modified

| File | Change |
| --- | --- |
| `backend/lait/domain/practice_session.py` | Four required saved fields on the frozen/slotted AttemptRecord projection. |
| `backend/lait/adapters/persistence/repositories.py` | Strict saved-array decoding and full AttemptRow-to-AttemptRecord mapping. |
| `backend/lait/application/queries/attempt_list_for_lesson.py` | Required fields on ListedAttempt and explicit forwarding through the public query. |
| `backend/lait/adapters/http/routers/practice.py` | Required list DTO fields and tuple-to-list mapping. |
| `backend/tests/adapters/http/test_http_dto_mapping.py` | Rich/empty/legacy fresh-app round trip, no-mutation snapshots and live-submit/list equivalence. |
| `backend/tests/adapters/persistence/test_lesson_reopen_reads.py` | Fresh-connection rich/empty records, legacy Unicode, order/duplicates, immutable snapshots and twelve malformed-payload cases. |
| `backend/tests/application/test_lesson_reopen_reads.py` | Complete explicit fake constructors and faithful query/no-mutation assertions. |
| `frontend/openapi.json` | Exported required feedback fields and nullable alternative; ignored generated input retained locally. |
| `frontend/src/api/generated/types.gen.ts` | Generated required attempt-list feedback fields and unit identity. |
| `01-17-SUMMARY.md` | Durable close-out and evidence for parent reconciliation. |

## TDD Gate Compliance

Task-level TDD applies to both tasks. Phase-level `TDD_MODE` is false in init/config, so the additional commit-enforcing MVP/TDD runtime gate is inactive. The user's explicit no-staging/no-commit instruction supersedes default RED/GREEN commit steps. Test evidence was recorded and checked before the corresponding implementation/generation.

| Task | RED evidence | GREEN evidence | Refactor |
| --- | --- | --- | --- |
| T1 backend tracer | Targeted suite: exit 1; 1 failed, 4 passed; target assertion found all four saved fields absent. `RED_EVIDENCE_OK`. | Same command: 5 passed; mandatory tracer reverify: 5 passed before T2. | New tests formatted and fixture connections explicitly closed; production behavior stayed green. |
| T2 contract expansion | Node target assertion: exit 1; 1 test, 1 failure; all four fields absent from the exported schema's required array. `RED_EVIDENCE_OK`. | Independent backend command: 28 passed; exporter/generator passed; same Node assertion: 1 passed; typecheck passed. | No additional source implementation needed for projection tests: T1 already supplies the behavior. |

T2's independent repository/query tests verify the proven T1 slice; its intentional RED tests the then-missing generated contract. No fixture crash, import error, collection error, unrelated failure or passing pre-implementation assertion was used as RED evidence.

### T1 RED evidence

- Command: `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests/adapters/http/test_http_dto_mapping.py -q`
- Target: `test_reopened_http_lists_complete_saved_feedback_without_mutation`.
- Expected: saved unit id, used/missed arrays and non-null alternative survive fresh SQLite-to-HTTP read.
- Actual assertion: `chunks_used=None`, `chunks_missed=None`, `natural_alternative=None`, `learning_unit_id=None`, while expected values were the stored unit id, `["rolling out"]`, `["follow through"]`, `"deploying the change"`.
- Exit code: 1. TAP: 5 tests, 4 pass, 1 fail, named target `not ok`.
- Checker: `node .codex/gsd-core/bin/gsd-tools.cjs check tdd-red-evidence tmp/gsd-01-17-evidence/t1-red.json --raw` → `passed:true, block:false, verdict:RED_EVIDENCE_OK, reason:target_test_failed`.

### T2 RED evidence

- Target: `generated_attempt_dto_requires_complete_saved_feedback`; exact Node command below.
- Expected: all four saved fields required in both OpenAPI and the generated type; natural alternative nullable.
- Actual assertion: `ERR_ASSERTION`, "all saved fields must be required in OpenAPI"; actual missing-field list contained `learning_unit_id`, `chunks_used`, `chunks_missed`, `natural_alternative`; expected missing-field list was `[]`.
- Exit code: 1. TAP: 1 test, 0 pass, 1 fail.
- Checker: `node .codex/gsd-core/bin/gsd-tools.cjs check tdd-red-evidence tmp/gsd-01-17-evidence/t2-red.json --raw` → `passed:true, block:false, verdict:RED_EVIDENCE_OK, reason:target_test_failed`.

## Verification

All commands ran with explicit repository workdir `D:/Helsing/gitHub/LAIT`. The bound root guard ran verbatim in Git Bash before the first write, using command-scoped safe-directory settings; it reported `ROOT_PIN_PASSED D:/Helsing/gitHub/LAIT`. No global Git settings changed.

| Command | Final result |
| --- | --- |
| `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests/adapters/http/test_http_dto_mapping.py -q` | 5 passed; tracer rerun also 5 passed before expansion. |
| `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests/adapters/persistence/test_lesson_reopen_reads.py backend/tests/application/test_lesson_reopen_reads.py backend/tests/application/test_practice_retry.py backend/tests/application/test_practice_finish_and_start_over.py -q` | 28 passed. |
| `.venv/Scripts/python.exe -B -m lait.adapters.http.export_openapi` | Exit 0. |
| `npm --prefix frontend run openapi:generate` | Exit 0; existing @hey-api/openapi-ts 0.99.0. |
| Generated DTO Node assertion below | 1 passed after generation. |
| `npm --prefix frontend run typecheck` | Exit 0, no compilation errors; no frontend fixture changes needed. |
| `.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider backend/tests -q` | 129 passed; zero skipped; one pre-existing Starlette/httpx deprecation warning. |
| `node frontend/node_modules/vitest/vitest.mjs run --root frontend src/registries/renderers/gapFillRenderer.test.tsx src/features/lesson/LessonWorkspacePage.test.tsx src/features/lesson/FocusPracticeMode.test.tsx` | 3 files, 44 tests passed. |
| Ruff check on all seven changed Python files | All checks passed. |
| Ruff format --check on four changed production files and the HTTP test | 5 files already formatted. |
| `git -c safe.directory=D:/Helsing/gitHub/LAIT diff --check` | Exit 0. |

The full backend run includes unchanged retry/corrected/repeat-copy/opening-score/finish/Start Over tests, public handler isolation, module/proof parity and the parent's untracked OpenAPI/Compose tests. The latter files were inspected/run and not edited.

Exact generated-contract test, used unchanged for RED and GREEN:

```powershell
node -e "const {test}=require('node:test'); const assert=require('node:assert/strict'); const fs=require('node:fs'); test('generated_attempt_dto_requires_complete_saved_feedback',()=>{ const schema=JSON.parse(fs.readFileSync('frontend/openapi.json','utf8')).components.schemas.AttemptListItemResponse; const fields=['learning_unit_id','chunks_used','chunks_missed','natural_alternative']; assert.deepEqual(fields.filter(field=>!schema.required.includes(field)),[],'all saved fields must be required in OpenAPI'); const types=fs.readFileSync('frontend/src/api/generated/types.gen.ts','utf8').split('export type AttemptListItemResponse = {')[1].split('};')[0]; for(const field of fields) assert.match(types,new RegExp(field+':'),'generated DTO must require '+field); assert.ok(schema.properties.natural_alternative.anyOf.some(type=>type.type==='null')); });"
```

## Dirty baseline preservation

Before writes, the executor captured the contents of the nine owned source/test/schema files plus the dirty generated SDK/index, `lessonApi.ts` and the workspace test fixture. Comparisons after generation showed:

- `sdk.gen.ts`, `index.ts`, `lessonApi.ts` and `LessonWorkspacePage.test.tsx` exactly match their captured pre-execution contents.
- The entire OpenAPI paths map matches its pre-execution contents. Only `components.schemas.AttemptListItemResponse` changed.
- The generated `practiceAdvance` binding is still present. Prior PracticeAdvance types and operation bindings were preserved.
- No delta in models, migrations, submit/advance/finish/Start Over handlers, evaluator/feedback module, renderer/workspace/stage state or dependency/lockfiles.
- Existing planning changes and unrelated untracked tests were left alone. Parent ownership of STATE/ROADMAP/REQUIREMENTS is retained.

Generation produced no additional SDK/index/client source delta requiring expanded ownership. No handwritten transport or generated-file hand edits were used.

## Threat mitigation and stubs

T-01-46: strict JSON string-array validation plus twelve corruption cases; no empty/null fallback and no corrupted row rewrite. T-01-47: exact saved attempt/unit identity and immutable snapshots through repository/query/HTTP; no retry-copy position inference. T-01-SC: no installs, dependency changes or provider calls.

No new endpoint, auth path, file-access surface or storage-schema boundary outside the plan's threat register was introduced. No new production stubs, TODO/FIXME, fabricated empty UI payload or skipped behavioral test was introduced. Genuine saved empty arrays/null are asserted as data.

## Decisions Made

Followed D-27/D-28/D-29/D-30/D-31 and the approved no-change assumption decision. Stored feedback is authoritative; reads never re-evaluate or rewrite legacy answers/explanations. Alternative generation remains outside this plan.

## Deviations from Plan

No implementation scope deviations. Total auto-fixed deviations: 0. No frontend compatibility deviation was needed.

Explicit execution overrides from the user were honored: no staging, commits, pushes, stashes, checkouts, resets or volume deletion; all authored edits used apply_patch; shared planning updates remain the parent's responsibility. Default commit and state-update steps were not run. These are authorized workflow overrides, not fabricated commit success or missing task work.

## Issues Encountered / Deferred observations

- Git Bash needed explicit invocation from PowerShell; the supplied guard then passed.
- Context7 MCP and ctx7 CLI were unavailable. No install was attempted; this narrow change follows existing in-project dataclass/DTO/TestClient/generator patterns and adds no version-dependent API.
- The optional full touched-file formatting diagnostic also identified two pre-existing multiline assertion layouts in the independent reopen test files. Those existing lines were left intact. New HTTP formatting was corrected, final production/HTTP format check passed, and all seven changed files pass Ruff lint.
- The existing Starlette/httpx deprecation warning remains out of scope; it did not fail any test.
- No authentication gate or task blocker occurred.

## Task Commits

T1, T2 and plan metadata: **uncommitted by explicit user instruction**. No git add/staging or commit command was run. Measured plan commits are 0; this authorized local-only execution must not be interpreted as a missing or successful commit. No worktree was created.

## User Setup Required

None.

## Next Phase Readiness

Ready for parent dispatch of **01-18** using the generated complete saved-feedback contract. Learner rendering, compact Details, disclosure gating, exact retry-copy restoration and deterministic explanation copy belong to 01-18 and were not implemented here. Existing empty-field restoration in the frontend is planned 01-18 work.

Backend 01-17 has no human checkpoint under the latest D-31/governance rule. The backend tracer was automatically reverified before expansion. The sole final blocking-human Docker feedback checkpoint belongs to 01-18, and the separate phase-close Docker learner-flow smoke/re-verification remain pending. No automated pass or this summary approves those human checks or closes EVAL-05/Phase 1.

## Self-Check: PASSED

- FOUND: all nine changed implementation/test/schema files and this summary on disk.
- VERIFIED: intentional T1/T2 RED assertions accepted as RED_EVIDENCE_OK; corresponding GREEN commands passed.
- VERIFIED: backend tracer reran successfully before T2; final backend 129/129 and focused frontend 44/44 passed.
- VERIFIED: generated schema paths and operation bindings preserved; SDK/index/API adapter/workspace fixtures equal the captured dirty baseline.
- VERIFIED: coverage classifier reports three backend deliverables, all_auto_covered:true, no errors. This does not approve the 01-18 human checkpoint.
- VERIFIED: measured commit count 0, unchanged HEAD, empty staged diff. No commit claims require a hash lookup.
- VERIFIED: no new stubs, untracked runtime outputs or out-of-plan threat surfaces; ignored local RED evidence is listed above.
- HANDOFF: parent owns shared planning updates; only 01-17 is complete. 01-18 and EVAL-05/Phase 1 closure remain pending.
