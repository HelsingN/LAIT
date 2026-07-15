# AI Language Coach

Modular, AI-assisted language-learning platform focused on converting passive knowledge into active speech through retrieval practice, lexical chunks, semantic feedback, and spaced repetition.

## Status

Pre-alpha repository skeleton prepared for GSD-driven discovery, architecture, planning, and implementation.

## Architecture direction

- Modular monolith
- Small Core
- Mod-First extension architecture
- Statically bundled trusted modules for MVP
- Public contracts for exercises, languages, AI providers, AI features, schedulers, importers, exporters, and future MCP adapters

## Repository layout

- `apps/` — deployable clients and services
- `packages/` — shared SDK, contracts, and UI packages
- `plugins/` — official and future community modules
- `docs/` — PRD, ADRs, research, and architecture documentation
- `docker/` — container-related assets
- `scripts/` — development and maintenance scripts
- `tests/` — cross-cutting and integration tests

## Documentation

- Product requirements: `docs/prd/PRD.md`
- Architecture decisions: `docs/adr/`
- Research: `docs/research/`
- Architecture: `docs/architecture/`
