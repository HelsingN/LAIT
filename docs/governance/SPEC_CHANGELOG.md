# LAIT Specification Changelog

This changelog records material changes to the planning/specification baseline. It is not the application release changelog.

## 0.2.0 — 2026-09-28

### Added

- Explicit planning/specification versioning policy.
- Immutable-history rule for accepted architectural decisions.
- Stable requirement-ID policy with explicit supersession for material requirement changes.
- Version baseline manifests under `docs/versions/`.
- Headless-capable application boundary as an architectural requirement for future integrations.
- MCP as the preferred future generic agent-integration adapter after the first working vertical learning slice.
- External AI orchestration model: an agent framework may decide how to conduct a learning session, while LAIT remains the authoritative learning engine and durable learning-state owner.

### Clarified

- FastAPI/Web UI are adapters/clients of application use cases rather than the semantic center of LAIT.
- DeepSeek Harness is a possible orchestration client, not a dependency of the LAIT core.
- Existing v1 roadmap scope is unchanged by these decisions.
- Production MCP remains deferred beyond v1, consistent with existing `INTG-01` and `MODL-12` requirements.

### Superseded

- None. Version 0.2.0 extends the 0.1.0 baseline without replacing the small-core Mod-First modular-monolith decision.

## 0.1.0 — historical baseline — 2026-09-28

This label identifies the repository planning state immediately before explicit version governance and the MCP/external-orchestration decisions were added.

Exact baseline commit:

`9c5a2c7c9a31ea84de280779ce12dcc3a2e0436b`

See `docs/versions/spec-v0.1.0.md`.