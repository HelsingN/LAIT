# Architecture Decision Records

ADR files preserve architectural reasoning across project evolution. Once an ADR is accepted, do not rewrite its semantic meaning in place. If the project changes direction, create a new ADR and link it through `Supersedes` / `Superseded by` metadata.

See `docs/governance/VERSIONING.md` for the complete policy.

## Naming

`ADR-001-short-title.md`

Numbers are permanent. Do not reuse a number after an ADR is rejected, deferred, or superseded.

## Required metadata

Each ADR should include:

- Status
- Date
- Spec version introduced
- Decision owners
- Supersedes
- Superseded by
- Related requirements

## Status lifecycle

`Proposed -> Accepted -> Superseded/Deprecated`

Alternative terminal states are `Deferred` and `Rejected`.

## Accepted decisions added in spec 0.2.0

- `ADR-013-specification-and-decision-versioning.md`
- `ADR-014-external-integration-boundary-and-mcp.md`
- `ADR-015-external-ai-orchestration.md`

## Reserved / initial candidate topics

The original architecture backlog remains valid and its numbers are intentionally left available for dedicated ADRs rather than being overwritten by the 0.2.0 additions:

1. Repository layout
2. Modular monolith
3. Module system and lifecycle
4. Capability Registry
5. Command Bus and Event Bus
6. Learning Unit model
7. Exercise Module API
8. Language Module API
9. AI Provider API
10. Scheduler API
11. Module-owned storage
12. Prompt versioning

These candidates are not automatically `Accepted`; their authoritative current behavior is still described by the existing PRD/planning/research baseline until a dedicated ADR is created.