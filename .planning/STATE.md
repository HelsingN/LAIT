---
gsd_state_version: "1.0"
milestone: v1.0
current_phase: 01
current_phase_name: Mod-First Manual Learning Loop
status: executing
stopped_at: Completed 01-08-PLAN.md
last_updated: "2026-10-02T00:40:12.098Z"
last_activity: 2026-10-01
last_activity_desc: Phase 01 execution started
state_head: 0f55d8851ba219963f0e7c6441940bde18a710c1
progress:
  total_phases: 9
  completed_phases: 0
  total_plans: 11
  completed_plans: 10
milestone_name: milestone
spec_version: 0.2.0
---

# Project State

## Project Reference

See: `.planning/PROJECT.md`
Current planning/specification baseline: `.planning/VERSION.md` (`0.2.0`)

**Core value:** A learner can turn their own professional English text into reliable progressive-retrieval practice that helps them recall and produce useful language independently.
**Current focus:** Phase 01 — Mod-First Manual Learning Loop

## Current Position

Phase: 01 (Mod-First Manual Learning Loop) — EXECUTING
Plan: 9 of 11
Status: Ready to execute
Current discussion area: Complete
Last activity: 2026-10-01 — Phase 01 execution started

Progress: [░░░░░░░░░░] 0%

## Performance Metrics

**Velocity:**

- Total plans completed: 0
- Average duration: —
- Total execution time: 0.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | - | - | - |

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

### Pending Todos

- Execute Phase 1 from `01-01-PLAN.md` through `01-11-PLAN.md`. Do not expand scope past `01-CONTEXT.md`.
- After a working vertical learning slice exists, consider a small MCP integration spike as an architectural acceptance test; do not add it to current Phase 1 scope.

### Blockers/Concerns

- Phase planning must resolve manifest v1 details, AI evaluation thresholds, scheduler parameters, and responsive interaction contracts at the phases where they first matter.
- No unresolved discussion blocker. Phase 1 planning is complete.
- Execution must preserve the Learning Unit, Gap Fill, proof-module, visibility, session, and application command/query decisions recorded in `01-CONTEXT.md`.
- Future MCP schemas and DeepSeek Harness packaging remain deferred and must not expand Phase 1 scope.

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| Integration | Production MCP adapter | Deferred beyond v1; architecture-ready only | Spec 0.2.0 |
| Integration | DeepSeek Harness plugin/package | Future reference integration candidate | Spec 0.2.0 |
| Domain | Decide whether `PracticeSession` becomes a first-class core entity | Deferred until concrete orchestration/practice requirements exist | Spec 0.2.0 |

## Session Continuity

Last session: 2026-10-02T00:40:12.045Z
Stopped at: Completed 01-08-PLAN.md
Resume file: None
