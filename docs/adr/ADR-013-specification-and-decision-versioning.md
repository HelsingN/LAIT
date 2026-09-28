# ADR-013: Specification and Decision Versioning

- **Status:** Accepted
- **Date:** 2026-09-28
- **Spec version introduced:** 0.2.0
- **Decision owners:** Project owner
- **Supersedes:** None
- **Superseded by:** None
- **Related requirements:** MODL-09 and project-governance concerns

## Context

LAIT is still in planning and early implementation. New product ideas, architectural directions, and integration opportunities can emerge before earlier assumptions are implemented. Editing old planning documents in place makes it difficult to distinguish original decisions from later reinterpretations and increases the risk of inconsistent requirements, roadmap drift, and accidental scope expansion.

Git history preserves bytes but does not by itself explain which historical planning state should be treated as a coherent baseline or why a decision changed.

## Decision

Introduce explicit planning/specification versioning and immutable decision history.

1. Maintain a project `spec_version` independent from executable release versions.
2. Record material specification baselines under `docs/versions/`.
3. Anchor historical baselines to exact Git commits where appropriate.
4. Treat accepted ADRs as historical records: do not change their semantic meaning in place.
5. When a decision changes, create a new ADR and mark the old decision superseded through metadata/indexing.
6. Keep requirement IDs stable. Materially changed requirements receive new IDs and explicit supersession links rather than silent replacement.
7. Record material planning changes in `docs/governance/SPEC_CHANGELOG.md`.
8. Use `.planning/VERSION.md` as the current-baseline pointer.

The detailed process is defined in `docs/governance/VERSIONING.md`.

## Alternatives considered

### Rely only on Git history

Rejected because commit history preserves content but does not provide an explicit semantic baseline or conflict-resolution policy.

### Copy every planning document into a versioned directory on every change

Rejected because it creates large duplicated documents and merge noise. Version manifests plus Git commit anchors provide exact recovery with less duplication.

### Continuously edit one canonical set of documents without version metadata

Rejected because it obscures when and why product/architecture assumptions changed.

## Consequences

### Positive

- Older decisions remain auditable.
- New ideas can be introduced without erasing earlier reasoning.
- Requirement and architecture conflicts become explicit.
- Planning changes can be reviewed atomically.
- External contributors and AI agents can identify the current baseline without guessing from file timestamps.

### Negative

- Every material planning change requires a small governance update.
- Some metadata duplication is intentional (ADR status, version manifest, changelog).
- Maintainers must distinguish spec version from product/API/schema versions.

### Risks

- Version numbers can become meaningless if bumps are performed for trivial edits or omitted for material changes.
- Old and new documents can still conflict if supersession metadata is not maintained.

## Validation

This decision is effective when:

- `.planning/VERSION.md` identifies the current specification baseline;
- historical and current baseline manifests exist;
- accepted ADRs declare the spec version introduced;
- future material decision changes use supersession rather than semantic overwrite.

## Related documents

- `.planning/VERSION.md`
- `docs/governance/VERSIONING.md`
- `docs/governance/SPEC_CHANGELOG.md`
- `docs/versions/spec-v0.1.0.md`
- `docs/versions/spec-v0.2.0.md`
