# Project Research Summary

**Project:** AI Language Coach
**Domain:** Local-first, AI-assisted progressive-retrieval language learning with Mod-First extensions
**Researched:** 2026-07-15
**Confidence:** HIGH

## Executive Summary

Research validates the PRD rather than displacing it. A React/TypeScript client, Python/FastAPI modular monolith, SQLite MVP store, Docker Compose deployment, small core, versioned public extension contracts, and trusted build-time bundled modules are a coherent architecture for a local single-user product. No major technical issue was found that requires changing the product vision or Mod-First direction.

The most important strengthening pattern is to implement the first learning workflow as durable vertical slices over real public contracts. Static registration is appropriate now; manifest validation, capability/category contracts, conformance tests, provenance, and official-module parity create the seam for runtime loading later. AI analysis and generation should be modeled as durable jobs, while attempts are persisted before semantic evaluation. Schema-constrained output is necessary but insufficient: source validation, deterministic-first grading, an explicit uncertainty state, learner overrides, and a human-curated regression corpus are required for trustworthy learning feedback.

The main risks are architectural coupling hidden behind “plugin” folders, lost source/prompt provenance, request-bound AI work, false confidence in semantic grading, inadequate attempt evidence for scheduling, SQLite misuse, prompt injection through pasted text, English assumptions leaking into core, and mobile interactions tested too late. These risks are preventable if their contracts and tests appear in the earliest phase that introduces the behavior.

## Guardrail: What Research Did Not Change

- The primary persona remains an adult B1–B2 IT professional learning English.
- The core value remains transforming user-owned professional text into active production practice.
- The MVP remains local, single-user, no-login, English-only, and responsive web.
- Gap Fill, Chunk Completion, Sentence Reconstruction, and Keyword Recall all remain required.
- The architecture remains a small-core Mod-First modular monolith with build-time bundled trusted modules.
- React, TypeScript, Python, FastAPI, SQLite, Docker, and Docker Compose remain product constraints.
- Runtime third-party loading, marketplace, sandboxing, external integrations, voice, and multi-language support remain deferred.

## Key Findings

### Recommended Stack

Use current stable, locked version lines: Python 3.14, FastAPI 0.139, Pydantic 2.13, SQLAlchemy 2.0.51+, Alembic 1.18, SQLite WAL, React 19.2, TypeScript 6.0.3, Vite 8.1, React Router 8.2, TanStack Query 5, Node 24 LTS, and Compose v2. TypeScript 7 is already available but is too early for this baseline because its stable programmatic API/tooling transition is incomplete; reevaluate later rather than making the project an ecosystem migration test.

Generate the frontend transport client from FastAPI's OpenAPI 3.1 document. Use JSON Schema for module manifests and AI feature outputs, SemVer for public extension APIs, uv plus a committed lockfile for Python, one JS lockfile, pytest/Vitest for unit and contract tests, and Playwright for desktop/mobile/browser workflow verification.

Do not add Redis/Celery for the local MVP. Introduce a small persisted job abstraction with one worker, idempotency, retries, progress, and terminal states. This preserves reliability now and leaves a replaceable queue adapter if hosted throughput later justifies another service.

### Expected Features

**Table stakes for the approved product:**

- Immutable/preserved lesson sources with explicit revisions and generated-artifact provenance.
- Visible, recoverable analysis and generation progress.
- Source-grounded learning-unit candidates with accept/edit/reject/manual-add control.
- Four progressive exercise types through registries and shared session contracts.
- Deterministic-first and semantic-fallback evaluation with uncertainty.
- Immutable attempts linked to target learning units, including retry/reveal/assistance evidence.
- Due review with a transparent simple scheduler and learner self-rating.
- Provider-outage degradation that preserves local lessons, attempts, and review.
- Responsive, accessible primary workflow and clear AI transmission disclosure.

**Differentiators to protect:**

- Progressive cue removal instead of recognition-only practice.
- Lexical chunks and professional source material rather than isolated generic vocabulary.
- Meaning-preserving paraphrase acceptance with short evidence-linked feedback.
- Weakness tracked at the learning-unit level across exercise types.
- Official modules using the same contracts intended for future community modules.

**Deferred:**

- Paragraph Recall until the four required modules and review loop meet quality gates.
- Advanced scheduling until simple-scheduler data demonstrates a limitation.
- Dynamic plugins, marketplace, external integrations, other languages, voice, auth/cloud, and new clients per the PRD.

### Architecture Approach

The core owns lessons, immutable source revisions, public learning-unit/exercise/attempt/evaluation/review envelopes, stable invariants, and ports. Application handlers own commands, queries, transactions, and idempotency. FastAPI, SQLAlchemy, provider transports, job execution, and the React shell remain adapters. Bundled modules register through a validated static catalog into typed category-specific capabilities; the registry is built atomically and frozen only after all manifests and dependencies pass.

Do not use one universal plugin interface or a generic service locator from domain code. Share manifest/lifecycle rules, then use narrow contracts for exercises, languages, AI providers, AI features, importers, and schedulers. Resolve capabilities at composition/application boundaries and inject typed collaborators.

Store core-owned data centrally and module-private data in typed module-owned tables or versioned settings. Avoid one SQLite database per module because cross-database atomicity and backup become harder. Use stable core IDs for allowed references, migrations owned by the responsible component, and no direct access to another module's private storage.

### Critical Pitfalls

1. **Paper-only modularity** — block core-to-module imports and type switches; prove extensibility with conformance tests and a no-core-change module.
2. **Lost provenance** — source revisions, analysis/generation runs, occurrence evidence, and prompt/schema/provider versions are required from the first AI slice.
3. **Request-bound AI** — persist commands/jobs, make them idempotent, and verify restart/retry behavior.
4. **Schema equals truth** — validate semantics/source references, calibrate against human labels, and retain `uncertain` plus learner override.
5. **Weak attempt semantics** — store every attempt, cue/reveal/retry state, unit coverage, and evaluator confidence before building scheduling.
6. **SQLite without operational discipline** — WAL on local storage, short transactions, busy timeout, controlled writes, checkpoint/backup tests, and a PostgreSQL migration threshold.
7. **Prompt injection through source material** — treat pasted text as untrusted data, separate it from instructions, deny tools, sanitize rendering, and add adversarial evals.
8. **English leakage and mobile-late design** — language capabilities own normalization; shared UI contracts include mobile/touch/accessibility behavior from the first exercise.

## Implications for Requirements

The PRD's product requirements should remain intact. Research suggests making the following reliability aspects explicit and testable in `REQUIREMENTS.md` rather than leaving them as invisible implementation details:

- Analysis and generation survive refresh/restart or fail recoverably without duplicating artifacts.
- Generated units/exercises retain source-revision and AI-run provenance.
- User input is persisted before AI evaluation, and provider failure never loses an attempt.
- Module manifests and category contracts are validated, versioned, and covered by conformance tests.
- Semantic evaluation is calibrated against a curated corpus and can return `uncertain`.
- Review evidence distinguishes independent success, retries, hints/reveal, and learner rating.
- Provider transmission is disclosed; secrets remain server-side; AI output rendering is sanitized.
- Docker Compose fresh-start, persistence/restart, mobile browser, and provider-outage behavior are acceptance tests.

These requirements strengthen delivery of existing FR/NFR/acceptance criteria; they do not add new product pillars.

## Implications for Roadmap

The final roadmap must derive phases from approved requirements and the selected project-structure mode. For the configured fine granularity, research supports approximately 9–11 dependency-aware phases. A vertical-MVP interpretation could use the following starting structure:

### Phase 1: Engineering and Public Contract Foundation
**Rationale:** Establish reproducible toolchains, Compose health, core/adapter dependency rules, manifest schema, module host, capability registry, and conformance harness before feature code creates private shortcuts.
**Delivers:** Running skeleton with static bundled-module activation and proof diagnostics.
**Avoids:** Paper-only modularity and dual contract truth.

### Phase 2: Lesson and Source Vertical Foundation
**Rationale:** Every later artifact depends on stable lesson identity and immutable source provenance.
**Delivers:** Create/manage lessons, pasted English source revisions, persistence, responsive shell, generated client.
**Avoids:** Lost provenance and mobile-late foundation.

### Phase 3: Durable Analysis and Learning-Unit Review
**Rationale:** Prove the first AI feature/provider separation and recovery model before multiplying AI calls.
**Delivers:** Job lifecycle, OpenAI-compatible provider, chunk-extractor feature, language-en support, source-grounded candidates, accept/edit/reject/add.
**Avoids:** Request-bound AI, prompt injection, schema-equals-truth.

### Phase 4: Exercise and Session Contract Slice
**Rationale:** Define the shared exercise envelope, renderer contribution, session state, and immutable attempt semantics with the simplest exercise.
**Delivers:** Gap Fill end to end with deterministic evaluation and attempt persistence.
**Avoids:** Renderer inconsistency and scheduler data gaps.

### Phase 5: Chunk Completion Module
**Rationale:** Validate a second exercise against the same public contracts and language normalization.
**Delivers:** Chunk Completion without core changes; expanded conformance suite.

### Phase 6: Semantic Evaluation and Sentence Reconstruction
**Rationale:** Introduce open-answer judgment only after attempts and deterministic paths are stable.
**Delivers:** Structured semantic evaluator, curated regression corpus, uncertainty/override, Sentence Reconstruction.
**Avoids:** Meaning/exactness grading failures.

### Phase 7: Keyword Recall and Progressive Session Flow
**Rationale:** Complete the four-module progression and prove renderer/generator/evaluator parity.
**Delivers:** Keyword Recall plus cue-level progression across exercise types.

### Phase 8: Weak-Unit Evidence and Review Scheduler
**Rationale:** Scheduling must consume real evidence from multiple exercise types rather than guessed fields.
**Delivers:** Weak-unit model, simple explainable scheduler, due queue, easy/difficult/mastered outcomes.

### Phase 9: AI Traceability, Privacy, and Graceful Degradation
**Rationale:** Consolidate cross-cutting provider metadata, disclosure, usage/cost, deletion, outage behavior, and safe rendering before acceptance.
**Delivers:** Auditable AI operations and usable local data without AI.

### Phase 10: Responsive Workflow and Release Hardening
**Rationale:** Verify the whole product under fresh install, restart, failure, concurrency, backup/restore, desktop, and mobile conditions.
**Delivers:** Docker Compose acceptance, browser matrix, performance/quality thresholds, proof extension module, and operational documentation.

### Phase Ordering Rationale

- Public contracts precede bundled implementations so official-module parity is real.
- Stable source identity precedes analysis; reviewed units precede exercise generation.
- Durable AI work precedes multiple AI features.
- Immutable attempt semantics precede semantic grading and scheduling.
- Closed exercises precede open evaluation, allowing deterministic infrastructure to stabilize first.
- The scheduler follows several exercise modules so weak-unit evidence is representative.
- Privacy/degradation and full hardening validate cross-cutting acceptance after all flows exist, while their hooks are added earlier.

### Research Flags for Phase Planning

- **Contract foundation:** Final manifest schema, permission vocabulary semantics, registry selection/override rules, and migration ownership need an ADR.
- **Analysis:** Source-length limit, candidate count defaults, chunk-selection rubric, prompt-injection test set, and job lease/retry semantics need phase research.
- **Semantic evaluation:** Human-labeled rubric, grammar-versus-meaning weighting, accepted-variant promotion, disagreement/uncertainty threshold, and model/provider test matrix need an AI-SPEC/eval plan.
- **Scheduling:** Exact simple algorithm, mastery semantics, and self-rating effects should be explicit and versioned; do not prematurely adopt FSRS.
- **Responsive exercises:** Each renderer needs UI-SPEC interaction/accessibility contracts, especially reconstruction on touch devices.
- **Privacy/deletion:** Retention and export/backup behavior need a documented policy before pilots contain personal professional text.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Core stack | HIGH | Current versions and compatibility verified from official sources. |
| Feature landscape | HIGH | Closely anchored to the detailed PRD and established retrieval/spacing research. |
| Mod-First architecture | HIGH | Static registration plus typed contracts is a low-risk MVP realization; runtime loading remains correctly deferred. |
| AI reliability pattern | HIGH | Structured validation, deterministic-first routing, provenance, evals, and uncertainty are well-supported; actual prompt/model quality remains empirical. |
| Simple scheduler details | MEDIUM | Spacing is well-supported, but parameter choices require product data and explicit acceptance criteria. |
| Semantic grading thresholds | MEDIUM | Architecture is clear; acceptable error/uncertainty rates require a labeled domain corpus and learner testing. |
| UX defaults | MEDIUM | Workflow is defined, but source limits, unit counts, progression, and feedback timing remain open research/product decisions. |

**Overall confidence:** HIGH

### Gaps to Resolve During Phase Planning

- Maximum source characters/tokens and chunking behavior.
- Default/maximum extracted learning units and confidence presentation.
- Exact progression rule between exercise types and definition of independent mastery.
- Semantic-evaluation rubric, uncertainty threshold, and human calibration set.
- Scheduler formula, intervals, and learner-rating effects.
- Module manifest v1 and whether command/event buses remain distinct abstractions internally.
- Module-owned relational migration naming and pre-1.0 compatibility policy.
- Deletion, backup/export, and AI trace retention behavior.
- Minimum screens and job progress/failure UX.

## Sources

### Primary and Authoritative

- [React versions](https://react.dev/versions), [Vite releases](https://vite.dev/releases), [Node releases](https://nodejs.org/en/about/previous-releases), and [TypeScript 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) — frontend baseline.
- [Python 3.14.6](https://www.python.org/downloads/release/python-3146/), [FastAPI releases](https://fastapi.tiangolo.com/release-notes/), [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/), [Alembic](https://alembic.sqlalchemy.org/en/latest/), and [Pydantic releases](https://github.com/pydantic/pydantic/releases) — backend baseline.
- [FastAPI SDK generation](https://fastapi.tiangolo.com/advanced/generate-clients/) and [OpenAPI](https://spec.openapis.org/oas/latest.html) — cross-language transport contracts.
- [Python plugin discovery](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/), [JSON Schema](https://json-schema.org/overview/what-is-jsonschema), and [SemVer](https://semver.org/) — extension contract path.
- [SQLite WAL](https://www.sqlite.org/wal.html), [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), and [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — operational constraints.
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), and [safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) — AI boundary and eval practices.
- [OWASP prompt-injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — untrusted source-content controls.
- [Retrieval-practice study](https://doi.org/10.1126/science.1152408), [distributed-practice meta-analysis](https://pubmed.ncbi.nlm.nih.gov/16719566/), [diminishing-cues study](https://pubmed.ncbi.nlm.nih.gov/28849580/), and [formulaic-sequence study](https://eric.ed.gov/?id=EJ805192) — learning-method support.

### Project Sources of Truth

- `docs/prd/PRD.md`
- `.planning/PROJECT.md`
- `.planning/config.json`

---
*Research completed: 2026-07-15*
*Ready for requirements and roadmap: yes*
