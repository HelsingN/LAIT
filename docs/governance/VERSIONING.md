# LAIT Specification and Decision Versioning Policy

## Purpose

LAIT is expected to evolve while implementation is still in progress. New product ideas, architectural decisions, requirements, and integration opportunities must be adoptable without erasing the reasoning that produced earlier plans.

This policy separates several kinds of versioning and defines how decisions are changed, superseded, and traced.

## Version Streams

### 1. Specification version

`spec_version` identifies the current planning baseline: product intent, accepted architectural decisions, requirements, and roadmap assumptions.

Use Semantic Versioning semantics adapted for a pre-1.0 specification:

- `0.x.0` — material planning change: new accepted architectural direction, new requirement family, changed scope boundary, or an intentional incompatible change to a prior planning assumption.
- `0.x.y` — clarification, typo correction, traceability improvement, or editorial change that does not alter intended behavior.
- `1.0.0` — reserved for the first stable specification baseline that corresponds to a product release whose public behavior is intentionally supported.

The current value is stored in `.planning/VERSION.md`.

### 2. Product/runtime version

The executable application will use its own release version. Do not use the planning `spec_version` as an application package version automatically.

### 3. Public contract/API versions

Module manifests, OpenAPI contracts, MCP tools/resources, and other extension contracts have independent compatibility versions. Their compatibility lifetime can be longer or shorter than the planning baseline.

Examples:

- module `apiVersion: 1`
- MCP surface `v1`
- OpenAPI schema/release version

### 4. Data/schema versions

Database migrations and module-owned schemas have their own ordered migration versions. They must not be inferred from product or specification version numbers.

## Immutable-history rule

A previously accepted decision is historical evidence. Do not rewrite its meaning in place.

When the project changes direction:

1. Create a new ADR.
2. State which ADR or assumption it supersedes.
3. Explain why the previous decision is no longer preferred.
4. Add the new ADR to the next specification baseline.
5. Update indexes/current-state documents to point to the newest active decision.

The old ADR remains readable. Only status/link metadata may be updated to identify its successor.

## ADR lifecycle

Allowed statuses:

- `Proposed` — being discussed; not authoritative.
- `Accepted` — active decision for the current baseline.
- `Deferred` — intentionally postponed; not active.
- `Rejected` — evaluated but not adopted.
- `Superseded` — was accepted, but a newer ADR now governs.
- `Deprecated` — still temporarily valid but scheduled for removal/replacement.

An accepted ADR should record:

- date;
- spec version introduced;
- decision owner(s);
- related requirement IDs;
- supersedes / superseded-by links where applicable;
- consequences and validation criteria.

## Requirement lifecycle

Requirement IDs are permanent identifiers.

### Editorial change

If wording changes without changing observable behavior, keep the ID and record the clarification in the specification changelog.

### Material change

If acceptance behavior, actor, scope, or compatibility meaning changes materially:

- do not silently rewrite the old requirement;
- create a new requirement ID;
- mark the old requirement `Superseded` in the relevant version manifest or requirement register;
- add an explicit `supersedes` link.

### New idea

A new idea does not immediately become a requirement. It moves through:

`Idea → Proposed requirement/ADR → impact review → Accepted/Deferred/Rejected → roadmap mapping`

This prevents interesting ideas from silently expanding an active phase.

## Version baseline manifest

Every material specification release gets a file under `docs/versions/`.

A version manifest records:

- inherited previous baseline;
- Git commit anchoring the previous exact state when relevant;
- ADRs introduced/superseded;
- requirement additions/removals/supersessions;
- roadmap impact;
- known unresolved questions.

Version manifests are summaries, not copies of every planning document. Git history provides exact content; manifests provide intent and traceability.

## Authority and conflict resolution

Different documents answer different questions:

- `docs/prd/PRD.md` — product intent and major scope.
- `.planning/REQUIREMENTS.md` — observable requirements and stable IDs.
- accepted ADRs — architectural/design decisions.
- `.planning/ROADMAP.md` — sequencing and delivery mapping.
- `.planning/STATE.md` — current execution position.
- `.planning/VERSION.md` and `docs/versions/*` — which planning baseline is current and what changed.

When two active documents conflict, do not silently reconcile them by editing both. Open a planning change, record the resolution in an ADR or version manifest, then update affected current documents together.

For an explicit supersession, the newer accepted ADR governs the decision it names as superseded. It does not automatically override unrelated PRD scope or requirements.

## Change workflow

For a material planning change:

1. Capture the idea and affected surfaces.
2. Check existing requirements and ADRs for conflicts.
3. Write a Proposed ADR and/or proposed requirement delta.
4. Decide whether the change affects the current phase, future phases, or architecture only.
5. Accept, defer, or reject it.
6. Bump `spec_version` if accepted and material.
7. Create/update the version manifest and changelog.
8. Update current-state pointers and roadmap/requirements only where the accepted decision actually changes them.
9. Keep the previous baseline recoverable by its manifest and Git commit.

## Branch and review convention

Material planning changes should normally be made on a dedicated branch and reviewed as one coherent pull request. This keeps related ADR, requirements, roadmap, and state changes atomic and makes conflicts visible before merge.

Suggested branch forms:

- `docs/spec-v0.3`
- `architecture/<topic>`
- `planning/<topic>`

## Current baseline

The first explicitly versioned baseline is `0.2.0`.

The immediately preceding repository state is designated historical baseline `0.1.0` and anchored at commit `9c5a2c7c9a31ea84de280779ce12dcc3a2e0436b`.