# Stack Research

**Domain:** Local-first AI-assisted language-learning web application with modular extension contracts
**Researched:** 2026-07-15
**Confidence:** HIGH for core stack; MEDIUM for optional supporting libraries

## Research Boundary

This research informs implementation without redefining the product. `docs/prd/PRD.md` and `.planning/PROJECT.md` remain authoritative. React, TypeScript, Python, FastAPI, SQLite, Docker Compose, the small-core Mod-First modular monolith, and build-time bundled modules are constraints rather than alternatives under evaluation.

## Recommended Stack

### Core Technologies

| Technology | Baseline | Purpose | Why Recommended |
|------------|----------|---------|-----------------|
| Python | 3.14.6 / `>=3.14,<3.15` | Backend runtime | Current bugfix line with support through 2030; SQLAlchemy and Pydantic have current Python 3.14 support. Lock the minor line for reproducible containers. |
| FastAPI | 0.139.x | HTTP/API adapter | Matches the PRD, produces OpenAPI 3.1, composes cleanly through routers/dependencies, and keeps HTTP outside domain/application services. |
| Pydantic | 2.13.x stable | Boundary validation and JSON Schema | Strong fit for request/response contracts, module manifests, AI structured outputs, and explicit validation errors. Do not use the 2.14 alpha line. |
| SQLAlchemy | 2.0.51+ within 2.0 | Persistence adapter | Mature typed ORM/Core with SQLite and PostgreSQL dialects; 2.0.51 is current and includes Python 3.14 fixes. Keep repository interfaces above it. |
| Alembic | 1.18.5+ within 1.x | Database migrations | Standard migration companion for SQLAlchemy; supports a governed path from SQLite to PostgreSQL. |
| SQLite | Runtime bundled with Python; WAL enabled | MVP relational store | Correct for one local learner and one-host deployment. WAL permits readers and a writer concurrently; short transactions, busy timeouts, backups, and checkpoint monitoring are still required. |
| React | 19.2.x, at least 19.2.7 | Responsive client | PRD constraint and current stable line. Use client-side SPA patterns; the product does not need React Server Components or SSR for MVP. |
| TypeScript | 6.0.3 | Client language | Current mature JS-based compiler with strict mode and modern ESM defaults. Defer TypeScript 7 until the wider toolchain no longer needs the TypeScript programmatic API. |
| Vite | 8.1.x | Frontend build/dev tool | Current supported line, simple SPA build, and explicitly recommended by React as a Create React App replacement path. |
| Node.js | 24 LTS | Frontend tool runtime | Production tooling should use LTS; Node 24 satisfies Vite 8 and current Playwright requirements. Do not target EOL Node 20. |
| Docker Compose | Current Compose v2 | Local orchestration | PRD constraint. Use health checks, named volumes, an explicit migration step, and one-command startup verification. |

### Supporting Libraries and Contracts

| Library / Standard | Version Line | Purpose | When to Use |
|--------------------|--------------|---------|-------------|
| React Router | 8.2.x | Client routing | Use declarative/data routing in SPA mode. Do not adopt experimental RSC behavior. |
| TanStack Query | 5.x | Server-state lifecycle | Use for API queries, mutations, cache invalidation, job-status polling, retries, and explicit error/loading states. Pin exact patches because its type fixes can ship in patches. |
| Zod | 4.x | Frontend-only runtime validation | Validate configuration or module-contributed frontend metadata when data is not already enforced by the generated API client. Avoid duplicating every Pydantic schema by hand. |
| OpenAPI 3.1 + generated TypeScript client | FastAPI-generated spec; generator pinned | Backend/frontend transport contract | Generate the client in CI and fail on a dirty diff or incompatible schema. Stable operation IDs are part of the public contract. |
| JSON Schema | 2020-12-compatible subset | Module manifest and AI-output schema | Define machine-checkable module manifests and provider-neutral structured outputs. Each provider adapter must declare the schema subset it supports. |
| SemVer | 2.0.0 | Public contract versioning | Version module API and manifests. Pre-1.0 may break intentionally, but compatibility checks and migration notes remain mandatory. |
| HTTPX | Compatible locked stable | Provider HTTP transport | Keep it inside AI provider adapters when an OpenAI-compatible REST transport is sufficient. A provider SDK may replace it only inside its adapter. |
| pytest | 9.x | Backend tests | Unit, application-service, repository, module-contract, migration, and provider-fake tests. |
| Vitest | 5.0.x | Frontend unit/component tests | Current regular-fix line aligned with Vite; use for registries, renderers, reducers, and contract adapters. |
| Playwright | Current pinned stable | Browser workflow tests | Test the complete learner journey on Chromium plus targeted WebKit and mobile emulation. |
| Ruff | Current pinned stable | Python lint/format | Fast, deterministic CI checks; configure centrally in `pyproject.toml`. |
| uv | Current pinned stable | Python project and lock management | Cross-platform lockfile and workspace support fit a Python modular monorepo; commit `uv.lock`. |

### Long-Running Work Pattern

Lesson analysis and exercise generation can outlive an HTTP request and may fail or be retried. Use a small durable job abstraction from the first AI feature:

1. HTTP command validates input and creates a `jobs` row plus domain intent in one transaction.
2. A single in-process worker claims queued jobs, records attempts, and invokes an AI-feature port.
3. Provider responses are validated before domain state is committed.
4. The client polls a job-status resource with TanStack Query; SSE can be added later behind the same status model.
5. Jobs expose `queued | running | succeeded | failed | cancelled`, progress steps, timestamps, safe error codes, retry count, and correlation ID.

This is intentionally smaller than Celery/Redis but more reliable than FastAPI `BackgroundTasks`, whose own documentation recommends larger task systems for heavy work. The job runner is an infrastructure adapter so a later Redis-backed worker does not change domain commands.

### AI Boundary Pattern

- `ai-provider-*` owns credentials, endpoints, rate-limit handling, transport errors, model identifiers, and provider-specific schema translation.
- `ai-feature-*` owns prompts, feature input/output models, prompt version, evaluation rubric, and retry policy.
- The feature requests a capability such as `ai.structured_generation`; it never imports a provider.
- The response is parsed and validated with Pydantic before any generated unit, exercise, or evaluation enters core-owned data.
- Persist provider, endpoint class, model, feature, prompt version, schema version, latency, token/usage fields, estimated cost, request correlation ID, and final disposition.
- Preserve explicit `uncertain` and `unable_to_evaluate` paths. Schema conformance does not imply semantic correctness.
- Maintain a fake deterministic provider for unit/integration tests and a curated regression corpus for real-provider evaluation.

## Suggested Repository Layout

```text
apps/
├── api/                         # FastAPI composition root and HTTP adapters
└── web/                         # React/Vite application shell
packages/
├── core/                        # dependency-light domain and application ports
├── sdk-python/                  # public backend extension contracts
├── contracts/                   # JSON Schema, manifest schema, OpenAPI snapshots
├── modules-python/              # bundled backend modules
│   ├── language_en/
│   ├── import_plain_text/
│   ├── learning_unit_lexical_chunk/
│   ├── exercise_gap_fill/
│   ├── exercise_chunk_completion/
│   ├── exercise_sentence_reconstruction/
│   ├── exercise_keyword_recall/
│   ├── ai_provider_openai_compatible/
│   ├── ai_feature_chunk_extractor/
│   ├── ai_feature_semantic_evaluator/
│   └── scheduler_simple/
└── modules-web/                 # matching renderers/editors, statically registered
generated/
└── api-client/                  # generated TypeScript transport client
tests/
├── contract/
├── integration/
└── e2e/
infra/
└── compose/                     # health checks, volumes, migration/start scripts
```

Keep one Python distribution initially if that makes packaging faster, but preserve these import boundaries. Separate publishable distributions are unnecessary until runtime installation is in scope.

## Development Tools and Quality Gates

| Tool / Gate | Purpose | Notes |
|-------------|---------|-------|
| `uv lock` / `uv sync --locked` | Reproducible backend environments | Pin Python minor and container base digest as well as Python dependencies. |
| npm lockfile with exact CI install | Reproducible frontend environments | Use one JS package manager; do not mix lockfiles. |
| OpenAPI snapshot + generated-client diff | Transport compatibility | Fail CI when backend contracts change without regenerated client and review. |
| Manifest JSON Schema validation | Extension compatibility | Validate every bundled manifest before application startup. |
| Module conformance suite | Official/community parity | Run the same public-contract tests against every module in a category. |
| Fake provider + golden eval corpus | AI repeatability | Unit tests never require paid network calls; gated live tests are separate. |
| Playwright desktop/mobile projects | Responsive workflow confidence | Test at least desktop Chromium, mobile Chromium, and mobile WebKit for the primary flow. |
| Docker Compose smoke test | Deployment acceptance | Fresh volume → migrations → health → lesson workflow; verify persistence after restart. |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Vite SPA | Next.js / React Router framework SSR | Only if public SEO, server rendering, or edge rendering becomes a product requirement. None is in the MVP. |
| Durable SQLite job table + one worker | Celery/Dramatiq + Redis/RabbitMQ | When multi-process throughput, horizontal workers, or distributed scheduling is actually needed. |
| SQLAlchemy 2.0 + Alembic | SQLModel | If a future prototype values reduced boilerplate more than strict separation of API, domain, and persistence models. |
| Generated OpenAPI client | Hand-written `fetch` wrappers | Only for a tiny spike; manual clients drift and undermine shared contracts. |
| Static registration table | Python package entry-point discovery | Use entry points when external installed packages become supported. The standard is a good future mechanism, not an MVP requirement. |
| CSS design tokens + scoped module styles | Heavy component framework | Adopt a framework only after UI-SPEC work demonstrates repeated primitives and accessibility needs it solves. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Create React App | Deprecated for new apps and a poor fit for current tooling | Vite 8 SPA |
| TypeScript 7 immediately | Newly released native compiler lacks the stable programmatic API some tools still consume | TypeScript 6.0.3, revisit after ecosystem validation |
| React Server Components for MVP | Adds server/client boundary and security complexity without serving the local SPA requirements | Standard React SPA |
| FastAPI `BackgroundTasks` for lesson analysis | In-process request-adjacent tasks are not a durable job system; restart loses work and heavy work competes with requests | Persisted job state plus replaceable worker adapter |
| Celery/Redis from day one | Adds services and operational failure modes before local single-user load justifies them | SQLite-backed single worker |
| Provider SDKs in core or AI-feature modules | Couples product intent to vendors and breaks replaceability | Provider adapter owns SDK/HTTP details |
| One generic `settings JSON` blob for all module data | Hides schema, indexing, migrations, ownership, and integrity | Core tables plus module-owned typed tables/documents with explicit schema versions |
| Dynamic code loading / marketplace plumbing | Explicitly excluded and destabilizes contracts before they are proven | Build-time bundled trusted modules |
| Redux as a default server-state cache | Duplicates TanStack Query responsibilities and encourages synchronization bugs | TanStack Query for server state; local component/context state for UI state |

## Version Compatibility Notes

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| Vite 8.1 | Node 20.19+ or 22.12+ | Choose Node 24 LTS; Node 20 is already EOL. |
| React 19.2 | TanStack Query 5 | Query supports React 18+; pin its patch because types may change in patches. |
| React Router 8.2 | Node 22.22+ for framework tooling | SPA runtime is browser-side; Node 24 LTS satisfies tooling. |
| TypeScript 6.0 | Vite 8 / React Router 8 | Explicit `types` and `rootDir` settings avoid TS 6 default surprises. |
| Python 3.14 | SQLAlchemy 2.0.51 / Pydantic 2.13.4 | Verify all locked transitive wheels on Linux container and Windows dev before committing the baseline. |
| FastAPI 0.139 | Pydantic 2 | Use Pydantic v2 models; do not introduce v1 compatibility paths. |
| SQLite WAL | One-host filesystem | Do not place the DB/WAL on a network filesystem; keep write transactions short and configure `busy_timeout`. |

## Sources

- [React versions](https://react.dev/versions) — verified React 19.2 and current patches.
- [React: sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app) — verified new-app direction.
- [Vite releases](https://vite.dev/releases) and [Vite 8 announcement](https://vite.dev/blog/announcing-vite8) — supported lines and Node requirements.
- [Node.js releases](https://nodejs.org/en/about/previous-releases) — Node 24 LTS and production LTS guidance.
- [TypeScript 6.0 announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) and [TypeScript 7.0 announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) — current compiler transition and API caveat.
- [Python 3.14.6](https://www.python.org/downloads/release/python-3146/) — current Python bugfix release.
- [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) — 0.139.0 current on 2026-07-01.
- [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/en/20/) — 2.0.51 current and Python 3.14 fixes.
- [Alembic docs](https://alembic.sqlalchemy.org/en/latest/) — 1.18.5 current.
- [Pydantic releases](https://github.com/pydantic/pydantic/releases) — 2.13.4 stable; 2.14 alpha excluded.
- [SQLite WAL](https://www.sqlite.org/wal.html) — concurrency, same-host constraint, and checkpoint risks.
- [FastAPI background-task caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/) — heavy-task boundary.
- [FastAPI SDK generation](https://fastapi.tiangolo.com/advanced/generate-clients/) — OpenAPI 3.1 and generated TypeScript client pattern.
- [Python plugin discovery](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/) — future entry-point discovery option.
- [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — JSON Schema and typed-output pattern.
- [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — health-based readiness.
- [Playwright installation](https://playwright.dev/docs/intro) and [emulation](https://playwright.dev/docs/emulation) — current browser/system support and mobile testing.
- [uv projects](https://docs.astral.sh/uv/guides/projects/) — cross-platform locking and project workflow.

---
*Stack research for: AI Language Coach*
*Researched: 2026-07-15*
