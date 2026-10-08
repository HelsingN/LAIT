---
gsd_state_version: "1.0"
milestone: v1.0
current_phase: 2
current_phase_name: AI-Assisted Learning-Unit Review
status: planning
stopped_at: Phase 01 merged in PR 3; historical audit cleanup prepared for a separate docs PR. Phase 2 ready to plan with explicit architecture evaluation.
last_updated: "2026-10-08T17:07:10.711Z"
last_activity: 2026-10-08
last_activity_desc: Phase 01 merged in PR 3; quick 261008-rko archives historical audits and reconciles current dispositions without implementation changes. Phase 2 ready to plan; original EVAL-05 partial/deferred to Phase 5.
progress:
  total_phases: 9
  completed_phases: 1
  total_plans: 19
  completed_plans: 19
  percent: 11
milestone_name: milestone
spec_version: 0.2.0
---

# Project State

## Project Reference

See: `.planning/PROJECT.md`
Current planning/specification baseline: `.planning/VERSION.md` (`0.2.0`)

**Core value:** A learner can turn their own professional English text into reliable progressive-retrieval practice that helps them recall and produce useful language independently.
**Current focus:** Phase 2 — AI-Assisted Learning-Unit Review (planning not started)

## Current Position

Phase: 2 — AI-Assisted Learning-Unit Review
Plan: Not started
Status: Ready to plan
Current discussion area: Not started; evaluate deferred architecture findings before MODL-06/MODL-07 and AI provider/feature boundaries
Last activity: 2026-10-08 — [PR #3](https://github.com/HelsingN/LAIT/pull/3) merged to main as 02013fc. Quick task 261008-rko preserves four local audit/pattern/UI reports and two earlier tracked review versions in dated history, reconciles current WR-02 as fixed and WR-01/WR-03 as open nonblocking advisories, and retains stable archive links. Phase 01 remains complete (19/19), verification passed 5/5, active UAT 76/76; original full EVAL-05 is partial/deferred to Phase 5. No implementation, completed-plan rerun or Phase 2 work; architecture notes retained. A separate docs PR is prepared for this cleanup.

Progress: [█░░░░░░░░░] 11%

## Performance Metrics

**Velocity:**

- Total plans completed: 19
- Average duration: —
- Total execution time: 0.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 19 | - | - |

**Recent Trend:**

- Last 5 plans: None
- Trend: Not started

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 18 min | 2 tasks | 53 files |
| Phase 01 P02 | 25 min | 3 tasks | 19 files |
| Phase 01 P03 | 48 min | 3 tasks | 18 files |
| Phase 01 P10 | 31 min | 2 tasks | 10 files |
| Phase 01 P04 | 17 min | 3 tasks | 11 files |
| Phase 01 P05 | 2h 38m | 2 tasks | 16 files |
| Phase 01 P06 | 10h 1m | 3 tasks | 23 files |
| Phase 01 P11 | 1h 45m | 1 tasks | 8 files |
| Phase 01 P07 | 24 min | 3 tasks | 17 files |
| Phase 01-mod-first-manual-learning-loop P08 | 33 min | 3 tasks | 32 files |
| Phase 01 P09 | 12 min | 3 tasks | 13 files |
| Phase 01 P12 | 35 min | 2 tasks | 11 files |
| Phase 01 P17 | 11 min | 2 tasks | 9 implementation/test/schema files + summary |

## Accumulated Context

### Decisions

Historical decisions remain recoverable through version manifests and ADR supersession. Current architectural additions are recorded in spec `0.2.0`.

Recent decisions affecting current and future work:

- [Roadmap]: Use vertical MVP slices rather than horizontal technical layers.
- [Roadmap]: Validate Mod-First boundaries through working learner workflows and public-contract proof slices.
- [Architecture]: Bundled modules use trusted build-time registration and receive no undocumented privileged access.
- [ADR-013]: Planning/specification baselines are versioned; accepted decisions are superseded rather than semantically overwritten.
- [ADR-014]: LAIT remains a standalone, headless-capable application; MCP is the preferred future generic agent-integration adapter and is not a v1 dependency.
- [ADR-015]: External agent frameworks may orchestrate tutoring/conversation, while LAIT remains the authoritative learning engine and durable learning-state owner.
- [Phase 01]: D-23 handler names are the published application boundary; HTTP only maps DTOs
- [Phase 01]: Omitted lesson title is suggested from the first meaningful line; a blank title stores Untitled Lesson
- [Phase 01]: Lesson source is capped at 100000 Unicode code points in the handler and the HTTP DTO
- [Phase 01]: lesson.list orders by created_at descending, then lesson id ascending
- [Phase 01]: D-21 confirmed: visibility stays on exercise contributions; Phase 1 values are learner and maintainer; experimental is rejected
- [Phase 01]: describe() allowlists public fields and marks every live catalog row active; list_visible_for filters on contribution visibility only
- [Phase 01]: Supported module api_version is 1; core.exercise-api 0.1.0 resolves dependency specs; runtime checks use Pydantic mirrored by the manifest schema
- [Phase 01]: learning_unit.remove sets removed_at and keeps the row; re-add inserts a new id
- [Phase 01]: Source span offsets are Unicode code points (Python str indices) in persistence and HTTP
- [Phase 01]: Unit commands call reject_if_unit_set_frozen, which reads has_open_practice_session and gets false until plan 01-05
- [Phase 01]: Learning-unit lesson foreign key is ON DELETE RESTRICT; this plan creates no ON DELETE CASCADE
- [Phase 01]: Compose build contexts are backend and frontend; uv.lock is copied from an additional workspace context
- [Phase 01]: API entrypoint runs Alembic upgrade head and only then execs uvicorn so /health cannot pass early
- [Phase 01]: Shared exercise types live in lait.domain.exercise so Gap Fill and proof implement one contract and core never names a module id
- [Phase 01]: Drag grading compares learning_unit_id. Matching chip text with a different id is incorrect
- [Phase 01]: Typed match is strip plus casefold on both sides. Internal space, punctuation, and apostrophes stay significant
- [Phase 01]: RESULT_CATEGORIES keeps acceptable, partial, and uncertain. Gap Fill returns only correct or incorrect
- [Phase 01]: The Gap Fill sentence window is the previous terminator or start through the next terminator or end, and it stays inside the module
- [Phase 01]: exercise.generate commits only completed or failed together with the accepted-unit id set
- [Phase 01]: practice.start rejects a stale accepted-unit set; a draft-only add does not invalidate the generation
- [Phase 01]: An open PracticeSession is the freeze flag; unit command modules stay unchanged
- [Phase 01]: N greater than 1 is drag then typed in span order; one accepted unit is typed only
- [Phase 01]: Attempt.learning_unit_id uses ON DELETE RESTRICT and copies the code-point span and unit text at submit
- [Phase 01]: Lesson workspace keeps the five stage labels mounted; loading and load errors render inside the open stage
- [Phase 01]: learning_unit.add receives Unicode code points; Start Practice enables only for the generated accepted-unit set
- [Phase 01]: Learner exercise types come from GET /api/exercise-registry?visibility=learner
- [Phase 01]: Create Lesson title is a two-line textarea; a blank title still stores Untitled Lesson
- [Phase 01]: practice.finish sets status closed and unfreezes because no open session remains
- [Phase 01]: practice.start_over sets status abandoned, keeps Attempt rows, then calls practice.start
- [Phase 01]: A refused practice.start after abandon restores the session to open so units stay frozen
- [Phase 01]: POST finish and start-over only map DTOs; the router does not call practice.start
- [Phase 01]: Focus Practice is a chrome swap on /lessons/:id; stage panels stay separate components
- [Phase 01]: The lesson page mounts rendererFor(exercise_type) only when that type is in the learner-visible list
- [Phase 01]: Exit Practice calls practice.finish; Start Over calls practice.start_over and does not assemble abandon-plus-start
- [Phase 01]: Workspace attempt rows are the submit responses kept in memory; Start Over does not clear them
- [Phase 01-mod-first-manual-learning-loop]: Pin @hey-api/openapi-ts at exactly 0.99.0 and use D-23 names as OpenAPI operationIds
- [Phase 01]: Maintainer removal deletes the proof manifest and the ProofRenderer registration only
- [Phase 01]: Proof removal tests use a temp manifest overlay and do not edit Core or application source
- [Phase 01]: Application tests do not import the FastAPI app; HTTP DTO tests live under adapters/http
- [Phase 01]: CI runs domain, persistence, and modules separately from the application suite, and still runs the full pytest gate
- [Phase 01]: practice.start returns the open session only when that session generation snapshot matches the current accepted set
- [Governance]: Learner-visible plans end on a blocking-human Docker check; backend-only plans do not. Observations are classified before they become blockers. See `docs/governance/MANUAL_UI_VERIFICATION.md`.
- [Phase 01]: UX-16/17 diagnosis is `01-13-DIAGNOSIS.md`. Follow-up plan `01-13-PLAN.md` is not executed. Slices 2–4 stay out of that plan.
- [Phase 01]: A repeat round stays in the same session. Queue identity is learning-unit id plus mode. The opening pass size is the score denominator. A named target resolves the copy at the cursor.
- [Phase 01]: Approved D-24–D-31 require compact submitted-once feedback, disclosure-safe Details and real persisted feedback restoration; see 01-17-CONTEXT.md. Retry rounds, score and Exit remain unchanged. PLAT-09 stays closed.
- [Phase 01]: D-32–D-37 supersede prior Details/content acceptance after a not-approved checkpoint: one inline accepted/wrong/revealed phrase and category, no duplicate input/card/Details. Detailed teaching/chunk/alternative display deferred to Phase 5; original EVAL-05 is partial, not complete. All 01-17/01-18 data/restore fixes and frozen domain behavior stay. Multi-blank/true drag-and-drop proposed Phase 4/9 only; see 01-18-FOLLOWUPS.md.

### Pending Todos

- Explicit execute-phase 01 --gaps-only and user option 3 authorized inline execution. Plans 01-01–01-18 are complete; final R2 T3 approved by user on 2026-10-07. Subsequent explicit Да authorizes scoped commit/push to existing origin/phase/01-execution; result belongs to Git history/handoff, not phase closure.
- Phase 1 merged in [PR #3](https://github.com/HelsingN/LAIT/pull/3), merge 02013fc. WR-02 fixed; verification passed 5/5, active UAT 76/76 with no blockers. [PR CI](https://github.com/HelsingN/LAIT/actions/runs/37722761625) and [push CI](https://github.com/HelsingN/LAIT/actions/runs/37722734237) passed on code head 01b205e. Audit cleanup is a separate docs PR, without new implementation or acceptance claims. Compact Feedback remains UX debt with no approved phase owner; original EVAL-05 is partial/deferred to Phase 5. Evaluate preserved architecture notes during Phase 2 planning before MODL-06/MODL-07 and AI boundaries.
- After a working vertical learning slice exists, consider a small MCP integration spike as an architectural acceptance test; do not add it to current Phase 1 scope.

### Blockers/Concerns

- Phase planning must resolve manifest v1 details, AI evaluation thresholds, scheduler parameters, and responsive interaction contracts at the phases where they first matter.
- No unresolved discussion blocker. Phase 1 planning is complete.
- Execution must preserve the Learning Unit, Gap Fill, proof-module, visibility, session, and application command/query decisions recorded in `01-CONTEXT.md`.
- Future MCP schemas and DeepSeek Harness packaging remain deferred and must not expand Phase 1 scope.
- Phase 1 completion returned one advisory: 01-17-SUMMARY includes a Vitest command parsed as a file reference. Actual test files exist and passing execution evidence is retained; this is metadata classification, not a missing implementation or Phase 1 PR blocker. See 01-CLOSURE.md.
- Architectural audit findings below do not block the Phase 1 PR. Do not perform speculative abstraction/refactoring during Phase 1 closure. When planning Phase 2, explicitly evaluate both findings before implementing MODL-06, MODL-07 and AI provider/feature boundaries. Preserve framework-independent application handlers, Core unaware of concrete module IDs, registry-based exercise discovery, the removable proof module, and the future peer HTTP/MCP adapter boundary. No ModuleHost design or new ADR is selected by these notes.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 261002-lpe | Recreated local Phase 1 UX audit with six findings and screenshot evidence | 2026-10-02 | Uncommitted — per user instruction | [261002-lpe-recreate-local-phase-1-ux-audit-from-cur](./quick/261002-lpe-recreate-local-phase-1-ux-audit-from-cur/) |
| 261005-sqr | UX-21: selection hint on the inactive Add button. Checkpoint not approved. | 2026-10-05 | Uncommitted — per user instruction | [261005-sqr-ux-21-show-the-empty-selection-hint-as-a](./quick/261005-sqr-ux-21-show-the-empty-selection-hint-as-a/) |
| 261005-u2f | Ignore local GSD runtime artifacts and milestone lock; files retained locally | 2026-10-05 | Uncommitted — no commit requested | [261005-u2f-ignore-local-gsd-runtime-artifacts-and-m](./quick/261005-u2f-ignore-local-gsd-runtime-artifacts-and-m/) |
| 261005-wza | Feedback collapsed on lesson entry; human checkpoint approved, task complete. | 2026-10-05 | Uncommitted — no commit requested | [261005-wza-collapse-feedback-by-default-when-openin](./quick/261005-wza-collapse-feedback-by-default-when-openin/) |
| 261008-8c0 | Archive historical Phase 1 UAT byte-for-byte and retain deferred architecture audit context | 2026-10-08 | — | [261008-8c0-archive-historical-phase-1-uat-and-retai](./quick/261008-8c0-archive-historical-phase-1-uat-and-retai/) |
| 261008-rko | Archive Phase 1 audit history and reconcile WR-02 disposition | 2026-10-08 | — | [261008-rko-archive-historical-phase-1-audit-reports](./quick/261008-rko-archive-historical-phase-1-audit-reports/) |

## Deferred Items

Items acknowledged for later work, including those carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| Integration | Production MCP adapter | Deferred beyond v1; architecture-ready only | Spec 0.2.0 |
| Integration | DeepSeek Harness plugin/package | Future reference integration candidate | Spec 0.2.0 |
| Domain | Decide whether `PracticeSession` becomes a first-class core entity | Deferred until concrete orchestration/practice requirements exist | Spec 0.2.0 |
| UX | Feedback current pass shows a heading, score, and plain labels. Hard phrases and a next-step panel were not in 01-15. | Landed in 01-15 | 2026-10-06 |
| UX | History rows still show the expected phrase in the stored explanation and again as the unit jump. The focus card does not. | Deferred. Not a 01-16 blocker. | 2026-10-06 |
| Learning feedback | Detailed teaching/chunk/alternative presentation from original EVAL-05 | Deferred to Phase 5; original EVAL-05 not fully delivered | D-32, 2026-10-07 |
| Exercise UX | Shared task with multiple blanks and actual drag-and-drop | Proposed Phase 4/9 follow-up; no current implementation | D-37, 2026-10-07 |
| Architecture | **Application/persistence port drift:** `LearningUnitRepository` no longer describes the full persistence contract used by application handlers. Practice, generation and attempt operations share the repository object, in several places with `# type: ignore[attr-defined]`. Application handlers remain independent of SQLAlchemy/FastAPI, so this is not a Phase 1 architecture failure. Continued expansion could turn the repository into a god port. Reassess whether narrower `ExerciseGenerationRepository`, `PracticeRepository` and `AttemptRepository` ports are warranted when the next phase adds persistence behavior. | Deferred evaluation during Phase 2 planning, before MODL-06/MODL-07 and AI provider/feature implementation; not a Phase 1 PR blocker or a selected refactor | Architectural audit, 2026-10-08 |
| Architecture | **Module resolution leakage into the application layer:** Exercise handlers depend on `lait.catalog.loader.load_generate/load_evaluate`, persist `module_package`, and resolve implementations through Python packages/importlib. Core remains module-ID agnostic and the Phase 1 proof-module seam works, so this is not a Phase 1 blocker. Before extending Mod-First to AI providers/features, reassess whether handlers should use an abstract ModuleHost/capability resolver instead of the concrete bundled loader, and whether durable records should reference stable module identity/version rather than a Python package as architectural identity. | Deferred evaluation during Phase 2 planning, before MODL-06/MODL-07 and AI provider/feature implementation; no premature ModuleHost design | Architectural audit, 2026-10-08 |

## Session Continuity

Last session: 2026-10-08T16:59:59Z
Stopped at: Phase 01 merged in PR #3. Historical audit cleanup prepared for a separate docs PR; Phase 2 ready to plan with deferred architecture evaluation before MODL-06/MODL-07/AI boundaries.
Resume file: .planning/phases/01-mod-first-manual-learning-loop/01-VERIFICATION.md
