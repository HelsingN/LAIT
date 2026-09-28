# Phase 1: Mod-First Manual Learning Loop - Research

**Researched:** 2026-09-28
**Domain:** Local walking skeleton — lesson paste, manual source-linked units, Gap Fill, public commands/queries, removable proof exercise, OpenAPI client diff
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### Learner path and screens
- **D-01:** The Lesson is the persistent primary workspace. The Lesson List is only the entry point.
- **D-02:** Stages are Source, Learning Units, Generate Exercises, Practice, and Feedback. Completing a stage unlocks and automatically expands the next stage. Every unlocked stage remains accessible and can be expanded or collapsed independently. Expanded and collapsed state is remembered per lesson.
- **D-03:** A title is suggested from the first meaningful source line or heading and is editable before creation. If no suitable title exists, use `Untitled Lesson`. The title is user-facing metadata only. Each lesson has an immutable internal ID.
- **D-04:** The full source is available in a collapsible panel. Learning units, exercises, and feedback show the relevant source excerpt with one-click navigation to that location in the full source.
- **D-05:** Starting practice enters a distraction-free Focus Practice Mode that shows only the exercise, feedback, and navigation. Ending practice restores the prior Lesson Workspace state. — **Reversibility:** costly — later exercise types and session modes reuse this workspace/practice split.
- **D-06:** Phase 1 uses clear panel and session-mode boundaries so later customization does not require a redesign.

### Manual learning-unit capture
- **D-07:** A Phase 1 learning unit is created only by selecting a span in the lesson source and pressing Add. The selection alone does not create a unit. Add with no selection does nothing. The stored unit text is exactly the selected span, and that span is the occurrence. The unit text is not editable in this phase (ANLY-06 is Phase 2).
- **D-08:** Add stores a draft. Accept moves the draft into the pool eligible for Gap Fill. Exercises are generated only from accepted units. — **Reversibility:** costly — Phase 2 AI candidates reuse draft/accepted.
- **D-09:** Before practice starts, the learner can add, delete, and re-add units. Delete applies to both drafts and accepted units. Spans must be disjoint. The same phrase in two non-overlapping places is two units. Touching edges are allowed. An overlapping selection is rejected and the existing unit stays.
- **D-10:** The unit set freezes when Focus Practice Mode starts. While that session is open, units cannot be added or removed. Closing the session returns to the Lesson Workspace and unfreezes the set. Starting over does not unfreeze the set and does not return to unit editing: it abandons the open session and starts a new practice session on the same accepted set.
- **D-11:** LLM generation of units from the source is Phase 2. It is not a Phase 1 mode.

### Gap Fill practice and feedback
- **D-12:** One accepted unit produces one Gap Fill item. The item shows the source sentence with only the current target unit's span blanked. Neighboring units in that sentence stay visible as ordinary text. The rest of the sentence is not modified.
- **D-13:** Gap Fill has two modes, both in this phase, both owned by `exercise-gap-fill`. Simple mode drags a chip into the blank. Hard mode types the unit. A session is two passes: every unit in drag mode, then the same units in typed mode. If the lesson has only one accepted unit, the drag pass is omitted.
- **D-14:** Drag chips are the current unit plus the other accepted units of the same lesson. The correct chip is that unit's identity, not a matching string. The correct chip is `correct`. Any other chip is `incorrect`.
- **D-15:** Both passes order items by span position in the source. Accept order is ignored. Equal positions use a stable secondary key, `learning_unit_id`.
- **D-16:** Typed answers match after trimming leading and trailing whitespace and ignoring case. Internal extra whitespace, punctuation, and apostrophes do not match. Full English normalization (EVAL-02) stays in Phase 3. — **Reversibility:** costly — later exercises inherit the Phase 1 comparison floor.
- **D-17:** Phase 1 Gap Fill emits only `correct` or `incorrect`. It does not emit `acceptable`, `partial`, or `uncertain`. A hit records the target chunk as used. A miss records it as missed.
- **D-18:** Explanation is required and deterministic. Natural alternative is nullable and may be absent. Templates: correct → `Correct. The expected answer is "{unit}".` Incorrect → `Your answer: "{submitted}". Expected: "{unit}".` Richer grammar explanation is later work.
- **D-19:** Recorded attempts are never deleted. Starting over drops only in-progress state that has not become an Attempt.

### Mod-First proof surface
- **D-20:** The proof exercise registers through the same public exercise contracts, static module catalog, and frontend renderer registry as Gap Fill. It does not appear in the normal learner workflow. Success means removing the proof module from the static catalog requires no Core or application changes, and Gap Fill plus LAIT still run. Tests can still instantiate the proof module and mount its renderer on maintainer/test paths.
- **D-21:** `visibility` is exercise-contribution metadata, not a field of the universal module manifest. Phase 1 values are `learner` (Gap Fill) and `maintainer` (proof). The lesson surface calls `exercise_registry.list_visible_for("learner")` and must not know the Gap Fill module id or special-case the proof module. Maintainer and conformance tests may read the full registry. `experimental` is a future value of the same field, not Phase 1 behavior. — **Reversibility:** one-way — contribution metadata is a published module contract; moving `visibility` onto the universal manifest later would touch every module category.
- **D-22:** MODL-02 is a documented read-only diagnostic query, `module_registry.describe()`. It is a different operation from the learner exercise list, not one endpoint filtered in the UI. It returns public registry metadata only: `module_id`, `module_version`, `category`, `capabilities`, and for exercise contributions `exercise_type`, `visibility`, `activation_status`. No private module internals. The lesson UI must not call it. There is no maintainer page in Phase 1. A process with an invalid catalog does not start, so every row in a live diagnostic has `activation_status: active`. Acceptance: the diagnostic shows Gap Fill and the proof module activated through the same public mechanism, while `visibility: maintainer` keeps the proof module out of the learner workflow.
- **D-23:** Phase 1 learner behavior goes through documented application commands and queries. HTTP handlers are transport adapters. They map request DTOs onto commands/queries and do not call repositories, registries, or module services directly. The same boundary is callable without HTTP. Phase 1 does not build a generic distributed command bus or an MCP adapter. An in-process typed handler boundary is enough. Replacing the FastAPI router with a future MCP adapter must not require changes to Core, the application workflow, or exercise modules. — **Reversibility:** one-way — command and query names are the application boundary ADR-014 preserves for peer adapters.

Commands:

```text
lesson.create
learning_unit.add
learning_unit.remove
learning_unit.accept
exercise.generate
practice.start
exercise.submit_attempt
practice.finish
```

Queries:

```text
lesson.get
lesson.list
learning_unit.list
practice.get
exercise_registry.list_visible_for("learner")
module_registry.describe
```

`module_registry.describe()` is maintainer diagnostics, not part of the learner workflow. `practice.finish` closes the session back to the workspace and unfreezes units. Start-over abandons the open session and opens another practice session without that unfreeze. Do not collapse those two outcomes into one unparameterized finish if finish means "return to the workspace".

### Claude's Discretion

- Represent start-over as abandon-plus-`practice.start` or as a distinct command intent. The learner-visible behavior is locked in D-10 and D-19. Do not delete attempts either way.
- Proof-module exercise body can be the smallest contract-valid generate/evaluate/renderer implementation. It must not be wired into the learner list.

### Deferred Ideas (OUT OF SCOPE)

- Full Workspace API and Workspace Module with movable, dockable, resizable panels, splits, tabs, saved layouts, and perspectives. Target later architecture work around Phases 6–8.
- Additional exercise-session modes such as Classic, Exam, Game, and Reading.
- LLM generation of learning units from the source. Phase 2.
- Editing unit text after capture. Phase 2 (ANLY-06).
- `visibility: experimental` as a live value. The field stays an enum that Phase 1 only accepts as `learner` or `maintainer`.
- A maintainer diagnostics page. Phase 1 is the `module_registry.describe()` query only.
- Full English answer normalization (whitespace, case, punctuation, contractions). Phase 3 (EVAL-02).
- Richer grammar explanation beyond the deterministic Gap Fill templates.
- MCP adapter implementation. The command/query boundary must be callable without HTTP, but the adapter is not built in this phase (ADR-014).
- Retry, reveal, and session resume. Later exercise phases.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| LESS-01 | Paste English plain text; no account or language setup | `lesson.create` stores immutable source + metadata title; single local learner |
| LESS-02 | List active lessons and open one | `lesson.list` / `lesson.get`; Lesson List is only the entry (D-01) |
| ANLY-08 | Manual unit linked to lesson and source occurrence | `learning_unit.add` stores exact span; no AI extraction |
| EXER-01 | Generate only from accepted units; recoverable status | `exercise.generate` reads accepted units; persist terminal status in the command transaction |
| EXER-02 | Start a session; one exercise at a time | `practice.start` / `practice.get`; Focus Practice Mode (D-05) |
| EXER-03 | Gap Fill via Exercise Registry | `exercise-gap-fill` + `list_visible_for("learner")` |
| EXER-07 | Submit, see feedback, continue in session | `exercise.submit_attempt`; attempts kept (D-19) |
| EVAL-01 | Deterministic closed-answer evaluation | Drag identity match; typed trim + casefold only (D-16) |
| EVAL-04 | One explicit result category | Persist the five-value category; Gap Fill returns only `correct` or `incorrect` (D-17) |
| EVAL-05 | Submitted answer, reference, explanation, used/missed chunks, optional natural alternative | D-18 templates; natural alternative null in Phase 1 |
| MODL-01 | Refuse startup on invalid catalog | Validate manifests before serving; invalid catalog does not start (D-22) |
| MODL-02 | Inspect active modules without private internals | `module_registry.describe()` only; lesson UI must not call it |
| MODL-03 | Add exercise module without Core edits | Proof module via static catalog + renderer registry (D-20) |
| MODL-12 | Commands/queries, no private table access | In-process handlers; HTTP is a peer adapter; no MCP (ADR-014) |
| PLAT-03 | Docker Compose migrates and becomes health-checked ready | Compose v2 healthcheck after Alembic |
| PLAT-09 | Generated TS client; CI fails on unreviewed drift | Export OpenAPI 3.1, regenerate, `git diff --exit-code` |
| PLAT-10 | Test core, persistence, and each module independently | Separate pytest targets; Vitest for renderer registry |
</phase_requirements>

## Summary

The repo has no application source. Phase 1 is the first implementation of the spec 0.2.0 boundary: React and FastAPI are adapters; the walking skeleton is the D-23 command/query list plus a static module catalog. MCP is a future peer of HTTP, not a deliverable. [VERIFIED: docs/versions/spec-v0.2.0.md:75] "HTTP and MCP are peer adapters over the same application use cases." [VERIFIED: docs/adr/ADR-014-external-integration-boundary-and-mcp.md:28] "MCP implementation is deferred until a working vertical learning slice exists; it is not a Phase 1 dependency."

Build one local learner loop: paste a lesson, add/accept a disjoint source span, generate one Gap Fill item per accepted unit, practice one item at a time (drag pass, then typed pass), and store attempts. A proof exercise uses the same contracts with `visibility: maintainer` and must be removable from the static catalog without Core changes.

**Primary recommendation:** Implement in-process typed handlers for the D-23 names, persist with SQLite/Alembic, expose them only through a thin FastAPI adapter, and prove catalog removal plus an OpenAPI client diff in CI. Do not add a command bus, a worker, or an MCP adapter.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Lesson paste, unit span rules, freeze, attempt retention | API / Backend (application handlers) | Database | Invariants must hold for non-UI callers (MODL-12) |
| Gap Fill blank, chip identity, typed compare, explanation templates | API / Backend (`exercise-gap-fill` module) | — | D-13 owns both modes in the module, not Core |
| `visibility`, catalog validation, `describe()` | API / Backend (registry) | — | Learner list and diagnostic query are different operations (D-22) |
| Lesson List, stage panels, Focus Practice Mode, drag/type UI | Browser / Client | — | D-01–D-06; UI must not own grading |
| Panel expanded/collapsed memory | Browser / Client | — | Chrome state; not a D-23 command |
| HTTP DTO mapping, OpenAPI, `/health` | API / Backend (FastAPI adapter) | — | Handlers stay callable without HTTP (D-23) |
| Migrations, lesson/unit/attempt rows | Database | — | Alembic on startup; no hand-edited SQLite |
| MCP tools | — | — | Out of scope. Do not add a tier or package |

## Project Constraints (from AGENTS.md)

- Frontend: React + TypeScript SPA. Backend: Python + FastAPI. DB: SQLite, WAL, Alembic path toward PostgreSQL.
- Hexagonal core: modules use public capabilities. Official modules get no private Core shortcuts.
- English-only processing; no language picker. One local learner; no login.
- Deterministic checks before any semantic evaluation. Phase 1 has no semantic evaluator.
- Source stays immutable in this phase. Secrets never reach the frontend or git. AI failure is irrelevant here because there is no provider call.
- Do not use FastAPI `BackgroundTasks`, Celery, Redis, provider SDKs, or a generic settings blob.

## Standard Stack

Versions below are the locked baseline. This pass did not re-query npm or PyPI. [CITED: .planning/research/STACK.md:17-44]

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.14.6 / `>=3.14,<3.15` | Backend | Locked runtime |
| FastAPI | 0.139.x | HTTP adapter only | OpenAPI 3.1; logic stays in handlers |
| Pydantic | 2.13.x stable (not 2.14 alpha) | Command/query DTOs, manifest validation | Boundary schemas |
| SQLAlchemy | 2.0.51+ within 2.0 | Persistence adapter behind repositories | SQLite now |
| Alembic | 1.18.5+ within 1.x | Migrations run by Compose before ready | PLAT-03 |
| SQLite | bundled; WAL + `busy_timeout` | One local learner | Named volume; not a network filesystem |
| React | 19.2.x, at least 19.2.7 | SPA | No RSC |
| TypeScript | 6.0.3 | Client | Strict |
| Vite | 8.1.x | SPA build | Node 24 LTS |
| Docker Compose | v2 | One-command migrate + health | PLAT-03 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| React Router | 8.2.x | `/` list and `/lessons/:id` workspace | SPA only |
| TanStack Query | 5.x (pin patch) | Lesson/unit/practice server state | Mutations call HTTP, which calls handlers |
| pytest | 9.x | Backend, contract, catalog tests | PLAT-10 |
| Vitest | 5.0.x | Renderer registry and focus-mode UI | Proof renderer mounts only in tests |
| Ruff | pinned stable | Lint/format | `pyproject.toml` |
| uv | pinned stable | Lockfile | Commit `uv.lock` |
| Zod | 4.x | Renderer contribution metadata only | Do not duplicate every Pydantic schema |

### Leave out of Phase 1

HTTPX, Playwright, AI provider SDKs, Celery, Redis. Playwright is PLAT-11 (later). HTTPX is for provider adapters (later).

**Installation:** Wave 0 creates `pyproject.toml` / `uv.lock` and the frontend lockfile from the table above. Do not add a package that STACK.md does not name.

## Package Legitimacy Audit

Registry legitimacy was not re-run in this pass (read scope was the phase sources only). No package outside STACK.md is recommended. None removed. None flagged SUS from this pass.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| Stack rows in the tables above | PyPI/npm as named in STACK.md | — | — | — | not re-checked | Approved only as already locked in STACK.md |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

The OpenAPI TypeScript generator is unnamed in STACK.md ("generator pinned"). Do not invent one here. The plan must pin a single generator and run the legitimacy gate before install. [ASSUMED]

## Architecture Patterns

### System Architecture Diagram

```text
Lesson List / Lesson Workspace / Focus Practice
        |  HTTP JSON (generated client)
        v
FastAPI routers  --map DTO-->  in-process command/query handlers
                                      |                |
                                      v                v
                                 repositories     exercise registry
                                      |           gap-fill | proof
                                      v                |
                                   SQLite              v
                                 (Alembic)     list_visible_for("learner")
                                               hides visibility=maintainer

module_registry.describe()  --> public metadata only (not used by lesson UI)
invalid catalog --------------> process refuses to serve

MCP adapter: not built. Same handlers are the future peer of FastAPI.
```

### Recommended Project Structure

```text
backend/
  lait/application/   # handlers named in D-23; no FastAPI imports
  lait/domain/        # lesson id, span, attempt; no module ids
  lait/adapters/http/ # routers + /health
  lait/adapters/persistence/
  lait/modules/exercise_gap_fill/
  lait/modules/exercise_proof/   # catalog entry only; Core must not import it
  lait/catalog/       # static manifests; startup validation
frontend/
  src/features/lesson/          # list, workspace stages, focus mode
  src/registries/renderers/     # exercise_type -> component
  src/api/generated/            # committed OpenAPI client
compose.yaml                    # migrate then serve; healthcheck
```

### Pattern 1: Handlers, not routers
Each D-23 name is a typed function. Routers only map DTOs. `practice.finish` unfreezes and returns to the workspace. Start-over calls `practice.start` again while a session is open: drop in-progress non-attempt state, keep Attempts, open a new session on the same frozen accepted set. Do not add a public command and do not overload `practice.finish`. [VERIFIED: .planning/phases/01-mod-first-manual-learning-loop/01-CONTEXT.md:49-73]

### Pattern 2: Visibility on the contribution
Universal manifest has no `visibility`. Contribution values are `learner` (Gap Fill) and `maintainer` (proof). Lesson UI calls `list_visible_for("learner")` and never branches on module id. Removal deletes the proof catalog entry and renderer registration only. [VERIFIED: 01-CONTEXT.md:43-46]

### Pattern 3: Synchronous generation record
`exercise.generate` writes Gap Fill items from accepted units in one transaction and stores a terminal status readable after restart. Empty accepted set stores failure and no items. No worker.

### Anti-Patterns to Avoid
MCP or a command bus; Core imports of module ids; browser-side grading; `BackgroundTasks` or Celery; a hand-written `fetch` client; one finish command for both leave and start-over.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP contract types | Manual client | Pinned OpenAPI generator + `git diff --exit-code` | PLAT-09 |
| Manifest checks | Ad-hoc dicts | Pydantic + JSON Schema subset at startup | MODL-01 |
| SQL strings | Hand-rolled driver | SQLAlchemy 2 + Alembic | Migrations are the startup path |
| Job queue | Worker, Redis | One DB transaction for generate | No long AI job in Phase 1 |
| Agent integration | MCP server | Callable handlers without HTTP | Spec peer-adapter rule |
| English normalization | Full EVAL-02 | Trim + casefold only | D-16 |

**Key insight:** The skeleton is a vertical slice of handlers and two catalog entries, not a platform.

## Common Pitfalls

| Pitfall | Avoid |
|---------|--------|
| English splitter in Core | Gap Fill owns the window: previous `.` `!` `?` (or start) through the next terminator (or end). Neighbor units in that window stay literal. Abbreviations may split early (A2). |
| Drag graded by string | Compare `learning_unit_id`. Same text in two places is two units (D-09, D-14). |
| Touching spans rejected | Overlap iff `start < other.end and other.start < end`. Reject `responsible for rolling out` overlapping `rolling out`; keep the existing unit. [VERIFIED: 01-CONTEXT.md:29,122] |
| `describe()` as the learner list | Lesson calls `list_visible_for("learner")` only. |
| Hard-coded Gap Fill id | Registry selects learner exercises. Removal test is the proof. |
| OpenAPI drift | Stable `operationId`s, committed client, CI diff. |

## Code Examples

```python
def typed_match(submitted: str, unit_text: str) -> bool:
    return submitted.strip().casefold() == unit_text.strip().casefold()
```

`Rolling out` matches `rolling out`. `rolling  out`, `rolling out.`, and `rolling out's` do not. Templates: `Correct. The expected answer is "{unit}".` and `Your answer: "{submitted}". Expected: "{unit}".` Natural alternative is null. Emitted category is only `correct` or `incorrect`; the stored type still allows `acceptable`, `partial`, and `uncertain` (EVAL-04). Order by span start, then `learning_unit_id`. One accepted unit skips the drag pass.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Routers own the workflow | Handlers under FastAPI; MCP is a later peer | spec 0.2.0 / ADR-014 | Tests call handlers with no ASGI app |

Do not build MCP in Phase 1 (ADR-014). Do not use FastAPI `BackgroundTasks` for generation (STACK.md).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Start-over reuses `practice.start` while a session is open; no new public command | Architecture | Planner may prefer a named abandon intent; behavior in D-10/D-19 stays either way |
| A2 | Gap Fill sentence window is terminator-based and lives in the module | Pitfalls | Abbreviation splits will look wrong; do not "fix" by moving the rule into Core |
| A3 | Generate commits a terminal status in-process; no job row lifecycle yet | Pattern 3 | If EXER-01 is read as a visible running state, add a status field, still not a worker |
| A4 | Stage collapsed state is `localStorage` keyed by lesson id | Responsibility map | A server preference would be extra scope |
| A5 | OpenAPI generator package is chosen in the plan, not here | Package audit | Wrong generator fails PLAT-09 |
| A6 | Ready probe path is `/health` returning 200 after migrations | Validation | Compose healthcheck must call whatever path the plan defines |

**If this table is empty:** N/A — confirmation needed for A1–A6 before they become locked.

## Open Questions

1. **OpenAPI generator package** — STACK requires a pinned generator and a dirty-diff failure [CITED: .planning/research/STACK.md:36] but does not name the package. The plan picks one, legitimacy-checks it, then locks the CI commands below.
2. **Non-terminal generate status** — EXER-01 needs a recoverable status. Persist it. Phase 1 may commit only `completed` or `failed`.

## Environment Availability

Not probed. Wave 0 must confirm Python 3.14.6, uv, Node 24 LTS, and Docker Compose v2. No in-repo fallback if any are missing.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Backend | not probed | 3.14.6 | — |
| uv | Locks, pytest | not probed | pinned | — |
| Node.js | Vite, Vitest, client gen | not probed | 24 LTS | — |
| Docker Compose v2 | PLAT-03 | not probed | v2 | — |

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.x (backend); Vitest 5.0.x (frontend) |
| Config file | none yet — Wave 0 adds `pyproject.toml` and Vitest config |
| Quick run command | `uv run pytest -q` and `npx vitest run` |
| Full suite command | `uv run pytest` and `npx vitest run` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LESS-01 | Create from pasted text, no account | unit | `uv run pytest tests/application/test_lesson_create.py -q` | ❌ Wave 0 |
| LESS-02 | List and open | unit | `uv run pytest tests/application/test_lesson_list.py -q` | ❌ Wave 0 |
| ANLY-08 | Add exact span; reject overlap; allow touching edges | unit | `uv run pytest tests/domain/test_spans.py tests/application/test_learning_unit_add.py -q` | ❌ Wave 0 |
| EXER-01 | Generate from accepted only; status stored | unit | `uv run pytest tests/application/test_exercise_generate.py -q` | ❌ Wave 0 |
| EXER-02 | One item; freeze set | unit | `uv run pytest tests/application/test_practice_start.py -q` | ❌ Wave 0 |
| EXER-03 | Gap Fill via registry; one unit skips drag | unit | `uv run pytest tests/modules/exercise_gap_fill/test_generate.py -q` | ❌ Wave 0 |
| EXER-07 | Submit, feedback, next item, session stays open | unit | `uv run pytest tests/application/test_submit_attempt.py -q` | ❌ Wave 0 |
| EVAL-01 | Identity drag; typed trim/casefold | unit | `uv run pytest tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ Wave 0 |
| EVAL-04 | Only `correct`/`incorrect` emitted | unit | `uv run pytest tests/modules/exercise_gap_fill/test_evaluate.py -q` | ❌ Wave 0 |
| EVAL-05 | Template explanation; null natural alternative; used/missed | unit | `uv run pytest tests/modules/exercise_gap_fill/test_feedback.py -q` | ❌ Wave 0 |
| MODL-01 | Invalid manifest prevents startup | unit | `uv run pytest tests/catalog/test_startup_validation.py -q` | ❌ Wave 0 |
| MODL-02 | `describe()` public fields; all live rows `active` | unit | `uv run pytest tests/catalog/test_describe.py -q` | ❌ Wave 0 |
| MODL-03 | Drop proof catalog entry; Core unchanged; Gap Fill runs | unit | `uv run pytest tests/catalog/test_proof_removal.py -q` | ❌ Wave 0 |
| MODL-12 | Handler suite without HTTP or table imports | unit | `uv run pytest tests/application -q` | ❌ Wave 0 |
| PLAT-03 | Compose healthy after migrate | smoke | `docker compose up -d --wait` | ❌ Wave 0 |
| PLAT-09 | Client matches OpenAPI | contract | `uv run python -m lait.adapters.http.export_openapi` then `npm run openapi:generate` then `git diff --exit-code -- frontend/src/api/generated` | ❌ Wave 0 |
| PLAT-10 | Core, persistence, modules split | unit | `uv run pytest tests/domain tests/adapters/persistence tests/modules -q` | ❌ Wave 0 |
| D-20 UI | Proof renderer mounts in Vitest only | component | `npx vitest run src/registries/renderers/proofRenderer.test.ts` | ❌ Wave 0 |

Handlers under `tests/application` must not start FastAPI. HTTP tests, if any, only assert DTO mapping.

### Sampling Rate

- **Per task commit:** `uv run pytest -q` and `npx vitest run`
- **Per wave merge:** `uv run pytest` and `npx vitest run` and `docker compose up -d --wait` and the OpenAPI diff command
- **Phase gate:** Full suite green, Compose healthcheck green, generated client diff empty

### Wave 0 Gaps

- [ ] `backend/tests/` layout — application, domain, catalog, modules, persistence
- [ ] `frontend` Vitest config and renderer registry test
- [ ] `compose.yaml` healthcheck that becomes ready only after Alembic
- [ ] `lait.adapters.http.export_openapi` plus `npm run openapi:generate`
- [ ] CI step that runs pytest, vitest, compose health, and `git diff --exit-code -- frontend/src/api/generated`

## Security Domain

One local learner. No login, no MCP, no provider secrets.

| ASVS | Applies | Control |
|------|---------|---------|
| V2 Authentication | no | No account (LESS-01) |
| V3 Session Management | no | Practice session is domain state, not a login session |
| V4 Access Control | yes | No private-table API; lesson UI does not call `describe()` |
| V5 Input Validation | yes | Pydantic; span inside source; overlap rejected |
| V6 Cryptography | no | No secrets in this phase |

Threats: out-of-range spans and string-equal drag grades (server checks id); SQL injection (SQLAlchemy binds); unexpected modules (static catalog, invalid manifest aborts); proof exercise leaking into the learner list (separate query).

## Sources

- HIGH: `01-CONTEXT.md`; `docs/adr/ADR-014-external-integration-boundary-and-mcp.md`; `docs/versions/spec-v0.2.0.md`; `.planning/ROADMAP.md` Phase 1; `.planning/REQUIREMENTS.md`
- MEDIUM: `.planning/research/STACK.md` lines 17–44 (not re-queried against registries)
- LOW: assumptions A1–A6

## Metadata

**Confidence breakdown:** Standard stack MEDIUM (STACK.md, registries not re-queried). Architecture HIGH (CONTEXT + ADR-014). Pitfalls MEDIUM (sentence window and generator package open).

**Research date:** 2026-09-28
**Valid until:** 2026-10-28
