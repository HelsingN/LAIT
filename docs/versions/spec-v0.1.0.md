# LAIT Specification Baseline 0.1.0

**Status:** Historical baseline
**Anchor date:** 2026-09-28
**Exact repository commit:** `9c5a2c7c9a31ea84de280779ce12dcc3a2e0436b`

## Purpose

This manifest gives the pre-versioning LAIT planning state an explicit identity without rewriting or duplicating its documents.

The exact contents of the baseline are the files at the anchor commit above, including:

- `docs/prd/PRD.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/*`
- `.planning/phases/*`
- `docs/adr/*`

## Architectural position

At this baseline LAIT is a small-core, Mod-First local-first modular monolith with:

- React/TypeScript web client;
- FastAPI backend adapter/composition layer;
- framework-independent core/application boundaries;
- trusted bundled modules registered at build time;
- versioned public extension contracts;
- capability registry restricted to composition/application boundaries;
- deterministic-first evaluation;
- durable jobs for long-running AI work;
- SQLite for the local MVP with a migration path to PostgreSQL;
- future adapter readiness for MCP and other integrations, but no production MCP deliverable in v1.

## Requirement state

The canonical requirements are those present in `.planning/REQUIREMENTS.md` at the anchor commit. Requirement IDs from this baseline remain stable identifiers under the versioning policy introduced later.

Notably, this baseline already contains:

- `MODL-12`: documented application commands/queries must be usable by integration developers without private database access, preserving a future MCP adapter boundary.
- `INTG-01`: production MCP adapter is deferred beyond the initial release.

## Supersession

This baseline is inherited by `0.2.0`. No core architectural decision from 0.1.0 is globally invalidated by 0.2.0; newer ADRs add governance and clarify the future agent-integration model.
