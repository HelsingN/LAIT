# Architecture Research

**Domain:** Mod-First local AI learning platform
**Researched:** 2026-07-15
**Confidence:** HIGH for modular-monolith boundaries; MEDIUM for final package names and job implementation details

## Constraint Preservation

The selected architecture is technically sound for the MVP. Research found no reason to replace the small-core Mod-First modular monolith. The recommendations below make its build-time implementation concrete while leaving a credible path to runtime modules later. They do not introduce microservices, dynamic third-party execution, or a marketplace.

## Recommended Architecture

### System Overview

```text
┌───────────────────────────────────────────────────────────────┐
│ React Application Shell                                      │
│ routes · lesson flow · session flow · review flow · settings  │
├───────────────────────────────────────────────────────────────┤
│ Frontend Module Host                                          │
│ renderer registry · editors · routes · panels · commands      │
├───────────────────────────────┬───────────────────────────────┤
│ Generated OpenAPI Client      │ Frontend Extension SDK        │
└──────────────────────┬────────┴───────────────────────────────┘
                       │ HTTP + job polling
┌──────────────────────▼────────────────────────────────────────┐
│ FastAPI Composition Root / Adapters                           │
│ routers · validation · error mapping · OpenAPI · health       │
├───────────────────────────────────────────────────────────────┤
│ Application Layer                                             │
│ commands · queries · transactions · authorization placeholder │
├───────────────────────────────────────────────────────────────┤
│ Core Kernel                                                   │
│ lessons · source revisions · units · attempts · reviews       │
│ public ports · domain events · invariants                      │
├───────────────────────────────────────────────────────────────┤
│ Backend Module Host                                           │
│ manifests · capability registry · command handlers · events   │
├───────────────────────────────────────────────────────────────┤
│ Bundled Modules                                               │
│ language · import · units · exercises · AI features/providers │
│ scheduler                                                     │
├───────────────────────────────┬───────────────────────────────┤
│ Persistence Adapters          │ Durable Job Runner             │
│ SQLAlchemy · SQLite · files   │ SQLite queue · worker · retry  │
└───────────────────────────────┴───────────────────────────────┘
```

### Dependency Rule

```text
adapters ──> application ──> domain
modules  ──> public SDK/ports ──> domain contracts
core never imports a concrete module, FastAPI, SQLAlchemy, React, or provider SDK
modules never import another module's private implementation or storage
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Core domain | Stable identities, invariants, value objects, domain events | Dependency-light Python packages; no ORM or HTTP annotations |
| Application services | Command/query orchestration, transactions, idempotency, port calls | Explicit handlers such as `CreateLesson`, `AnalyzeLesson`, `SubmitAttempt` |
| Public extension SDK | Capability types, registration interfaces, manifest model, shared errors | Versioned Python protocols/ABCs and TypeScript interfaces |
| Backend module host | Validate manifests, register bundled modules, resolve capabilities, record activation | Explicit static module catalog at startup |
| Frontend module host | Register exercise renderers/editors/routes/panels by typed contribution | Static imports assembled by build-time catalog |
| Capability registry | Resolve one or more providers for declared capability IDs | Typed registry with duplicate/missing dependency validation |
| Command bus | Dispatch named application commands across core/module boundary | In-process typed dispatcher; not a generic distributed broker |
| Event bus | Publish post-commit domain/application facts | In-process subscribers; outbox only when external delivery appears |
| Persistence | Map repositories/unit of work to SQLAlchemy and SQLite | Core-owned tables plus module-owned typed tables with migration ownership |
| Job runner | Execute slow AI work durably and expose state | Persistent job table, leases, retry/backoff, single worker process/thread |
| AI-feature modules | Feature prompts, rubrics, input/output schemas, prompt versions | Call provider capability; validate output; never own credentials |
| AI-provider modules | Model transport, credentials, usage, provider errors | HTTP/SDK adapter behind provider-neutral capabilities |
| Language module | Tokenization, normalization, punctuation, stop words, direction metadata | `language-en` implementation of documented language ports |
| Scheduler module | Convert evidence to due date/state | `scheduler-simple` pure policy with versioned parameters |

## Domain and Data Ownership

### Core-Owned Data

- `lessons`, `source_revisions`, and lesson metadata
- `learning_units`, source occurrences, acceptance state, and provenance
- `exercise_definitions` / `exercise_instances` envelope and module type/version
- `attempts`, submitted answers, assistance/reveal flags, and evaluation association
- `evaluation_results` normalized category and trace link
- `review_items`, due state, scheduler module/version, and outcomes
- `module_registrations`, manifest hash, API version, activation state
- `jobs` and AI request trace envelopes when they affect core workflow reliability

### Module-Owned Data

- Exercise-specific payloads that cannot fit the public envelope without leaking internals
- AI prompt templates, feature configuration, and cached feature results
- Language-specific analysis metadata
- Scheduler-specific state beyond the core due-date contract

Each module owns its migration namespace and may access core data only through a documented repository/query capability. Cross-module foreign keys should target stable core IDs, never another module's private table. Avoid a separate SQLite database per module in MVP: cross-database atomicity in WAL mode is not guaranteed, and backup/migration becomes harder.

### Source and Generated-Artifact Provenance

Use immutable source revisions:

```text
Lesson 1 ──> SourceRevision N
                ├──> AnalysisRun(prompt/schema/provider metadata)
                ├──> LearningUnitOccurrence(offsets + excerpt)
                └──> ExerciseGenerationRun
```

Editing a lesson creates a new revision. Existing units/exercises remain auditable against the prior revision; the UI can offer explicit re-analysis rather than silently mutating them.

## Module Contract Pattern

### Manifest Minimum for MVP

```yaml
id: official.exercise.gap-fill
name: Gap Fill
version: 0.1.0
apiVersion: 1
publisher: ai-language-coach
category: exercise
backendEntrypoint: packages.modules_python.exercise_gap_fill.plugin:create_module
frontendContribution: exercise-gap-fill
capabilities:
  provides: [exercise.generate.gap-fill, exercise.evaluate.gap-fill]
  requires: [core.exercise-api@1, language.normalize@1]
permissions: [lesson.read, learning-unit.read, attempt.write]
dataSchemaVersion: 1
```

Validate manifests with Pydantic and a checked-in JSON Schema. During build-time registration, entrypoints are symbolic catalog keys, not arbitrary file paths loaded from user input. Reserve Python package metadata entry points for the future external-package loader.

### Activation Sequence

1. Import the fixed bundled module catalog.
2. Parse and validate each manifest against API version and category schema.
3. Reject duplicate IDs/capabilities and unresolved required capabilities.
4. Run module registration into a temporary registry.
5. Freeze the registry only after all registrations succeed.
6. Persist active manifest IDs, versions, and hashes for traceability.
7. Expose a read-only module/capability diagnostic endpoint.

A failed module must not leave half-registered capabilities.

### Category-Specific Contracts

Do not create one universal plugin interface. Share lifecycle and manifest rules, then define narrow category contracts:

- `ExerciseGenerator`, `ExerciseEvaluator`, `ExerciseRendererContribution`
- `LanguageNormalizer`, `Tokenizer`, `LanguageMetadata`
- `StructuredGenerationProvider`, `TextGenerationProvider`, future speech capabilities
- `ChunkExtractor`, `SemanticAnswerEvaluator`
- `Importer`
- `ReviewScheduler`

This preserves type clarity and prevents a generic service locator from becoming an undocumented backdoor.

## Command and Event Semantics

### Commands

Commands express user/application intent, return a result, and have one transaction owner. Initial names from the PRD are appropriate, with explicit request IDs for idempotency:

```text
lesson.create
lesson.update_source
lesson.request_analysis
learning_unit.accept | edit | reject | add
exercise.request_generation
exercise.submit_attempt
review.start | review.record_outcome
```

### Events

Events state facts after successful commit. Handlers must tolerate duplicate delivery even though the MVP bus is in process:

```text
lesson.created
lesson.source_revised
analysis.requested | completed | failed
learning_unit.accepted
exercise.generated
attempt.submitted | evaluated
review.scheduled | completed
module.activated
```

Publish post-commit. Never let an event handler mutate the same aggregate inside an implicit nested transaction. If external integration arrives later, introduce an outbox behind the event publisher without changing domain events.

## Key Data Flows

### Lesson Analysis

```text
Paste text
  → HTTP validates length/encoding
  → Create lesson + immutable source revision
  → lesson.request_analysis (idempotency key)
  → persist queued job
  → worker resolves ai.feature.chunk-extraction
  → feature resolves ai.structured-generation provider
  → schema validation + source-offset validation
  → persist AnalysisRun + candidate units atomically
  → analysis.completed
  → UI polling observes result and opens unit review
```

If the provider fails, the job records a retryable/non-retryable error and the lesson remains intact. A retry creates a new attempt on the same logical job or a replacement job linked to it; it must not duplicate accepted units.

### Exercise Generation

```text
Accepted units
  → select exercise capability from registry
  → validate module dependencies and source revision
  → deterministic template generation where available
  → AI feature only where needed
  → validate module payload schema
  → persist envelope + typed payload + provenance
  → renderer registry chooses UI by exercise type/apiVersion
```

### Attempt and Evaluation

```text
Submit answer
  → persist immutable Attempt (answer + timing + assistance state)
  → exercise evaluator chooses deterministic path first
  → optional semantic evaluator returns structured result
  → validate status/evidence/target-unit references
  → persist EvaluationResult
  → update weak-unit evidence
  → scheduler computes review transition
  → return concise feedback
```

Persist the attempt before an AI evaluation call so provider failure cannot lose the learner's work. The evaluation may move from `pending` to `completed` or `unable_to_evaluate`.

## API and Frontend Boundaries

- FastAPI schemas are transport DTOs; map them to application commands and domain values rather than using them as domain entities.
- Generate an OpenAPI 3.1 TypeScript client. Stable, explicit operation IDs and schema names are reviewed public surfaces.
- TanStack Query owns remote state; React components own ephemeral interaction state. Avoid a second global copy of lessons/attempts.
- Frontend exercise modules receive a versioned `ExerciseInstance` envelope and submit through a shared attempt command, not custom endpoints unless the category contract explicitly permits one.
- Module UI contributions must declare accessibility metadata and provide loading, error, readonly/review, and mobile behavior.
- Start with job-status polling. The API shape can later support SSE without changing job identity or terminal states.

## Project Structure

```text
apps/
├── api/src/lait_api/
│   ├── main.py                    # composition root only
│   ├── routers/                   # HTTP adapters by capability
│   ├── schemas/                   # transport DTOs
│   ├── error_mapping.py
│   └── health.py
└── web/src/
    ├── app/                       # shell, routes, providers
    ├── features/                  # lesson/session/review flows
    ├── module-host/               # contribution registries
    ├── shared/                    # accessible UI primitives
    └── generated/                 # API client
packages/
├── core/src/lait_core/
│   ├── domain/
│   ├── application/
│   ├── ports/
│   └── events/
├── sdk-python/src/lait_sdk/
│   ├── manifest.py
│   ├── capabilities.py
│   ├── exercises.py
│   ├── language.py
│   ├── ai.py
│   └── scheduler.py
├── contracts/
│   ├── module-manifest.schema.json
│   ├── exercise-envelope.schema.json
│   └── openapi.snapshot.json
├── modules-python/
└── modules-web/
infra/
├── migrations/
├── compose.yaml
└── docker/
tests/
├── unit/
├── contract/
├── integration/
├── ai-evals/
└── e2e/
```

## Architectural Patterns

### Capability Registry, Not Generic Service Locator

**What:** Modules register typed providers under versioned capability IDs; consumers declare the capability interface they require.

**When:** Cross-category extension points such as AI structured generation, language normalization, and exercise generation.

**Trade-offs:** Excellent replaceability and diagnostics; requires explicit duplicate/selection policy and can become opaque if arbitrary code resolves capabilities everywhere. Restrict resolution to composition/application boundaries.

```python
provider = registry.require(
    CapabilityId("ai.structured_generation", api_version=1),
    StructuredGenerationProvider,
)
```

### Ports, Adapters, and Per-Command Unit of Work

**What:** Application handlers depend on repository/provider ports; FastAPI, SQLAlchemy, and provider SDKs implement adapters.

**When:** All core workflows.

**Trade-offs:** Adds mappings and interfaces, but it is the minimum discipline needed to prove provider/database/module replaceability. Do not abstract pure internal helpers without a boundary reason.

### Durable Process Manager for AI Work

**What:** Long-running workflows persist job state and advance through explicit steps.

**When:** Analysis, AI-heavy exercise generation, and potentially semantic batch evaluation.

**Trade-offs:** More states and tests than awaiting a provider call, but gives retry, refresh recovery, observability, and data safety. Keep the first runner single-process.

### Contract Tests as Extension Governance

**What:** Each category SDK ships a conformance suite every official module must pass.

**When:** From the first two modules in a category.

**Trade-offs:** Test maintenance becomes part of API evolution, which is exactly the intended cost of a public extension contract.

## Scaling and Evolution

| Context | Architecture Adjustment |
|---------|-------------------------|
| Local single user / MVP | One API, one worker, SQLite WAL, static modules, polling; optimize for correctness and recovery. |
| Hosted small deployment | PostgreSQL adapter, separate worker process, object storage for large sources, rate limits; keep one modular monolith. |
| Higher AI throughput | Redis/database queue or managed jobs, per-provider concurrency limits, caching, batch APIs; no domain split required. |
| External modules | Signed packages, entry-point discovery, permission enforcement, compatibility resolver, isolated frontend delivery; only after contracts stabilize. |
| Multiple teams / hotspots | Split a service only when ownership, scaling, or failure isolation data demonstrates a boundary; preserve commands/events as seams. |

The first bottleneck is likely provider latency/rate limits, not FastAPI or SQLite reads. The second is SQLite write contention if AI jobs and attempts write concurrently at hosted scale. Neither justifies microservices in the local MVP.

## Anti-Patterns

### “Plugin” Means a Folder Convention Only

**Failure:** Modules exist in folders but core imports their classes, reads their tables, or switches on exercise type.

**Better:** Public category contracts, manifest validation, registries, and a proof module added without core changes.

### Capability Registry Everywhere

**Failure:** Domain code locates dependencies dynamically, hiding required collaborators and creating runtime-only errors.

**Better:** Resolve at composition/application boundaries and inject typed dependencies into handlers.

### Dual Source of Contract Truth

**Failure:** Pydantic models and TypeScript interfaces evolve manually and disagree.

**Better:** OpenAPI/JSON Schema is generated or checked from an authoritative backend contract and the TypeScript client is regenerated in CI.

### Event Bus as Transaction Magic

**Failure:** Handlers synchronously cause hidden writes, recursive events, and partially committed state.

**Better:** One transaction owner per command; publish facts post-commit; make follow-up work explicit and idempotent.

### Universal JSON Payloads

**Failure:** Every module stores arbitrary blobs and validation moves to ad hoc runtime code.

**Better:** A small public envelope plus category/module schemas and typed storage when query/integrity needs justify it.

## Sources

- [Python Packaging: creating and discovering plugins](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/) — future package-entry-point mechanism.
- [Python entry-points specification](https://packaging.python.org/en/latest/specifications/entry-points/) — standardized installed-component advertisement.
- [FastAPI SDK generation](https://fastapi.tiangolo.com/advanced/generate-clients/) — OpenAPI 3.1 and generated TypeScript client.
- [JSON Schema overview](https://json-schema.org/overview/what-is-jsonschema) — declarative structure, constraints, documentation, and validation.
- [Semantic Versioning 2.0.0](https://semver.org/) — public compatibility vocabulary.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — transport-contract standard.
- [SQLite WAL](https://www.sqlite.org/wal.html) — concurrency, same-host, atomicity, and checkpoint implications.
- [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) — heavy-work caveat.
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — schema-constrained provider-output pattern.
- `docs/prd/PRD.md` and `.planning/PROJECT.md` — authoritative architecture and product constraints.

---
*Architecture research for: AI Language Coach*
*Researched: 2026-07-15*
