# LAIT Planning / Specification Version

**Current spec version:** `0.2.0`
**Status:** Current planning baseline
**Updated:** 2026-09-28

This version identifies the project planning/specification baseline. It is intentionally separate from future executable product releases, public API versions, module contract versions, and database schema versions.

## Baselines

| Spec version | Date | Meaning | Reference |
|---|---|---|---|
| `0.1.0` | 2026-09-28 | Historical baseline before version-governance and external AI-orchestration decisions were introduced | Git commit `9c5a2c7c9a31ea84de280779ce12dcc3a2e0436b` and `docs/versions/spec-v0.1.0.md` |
| `0.2.0` | 2026-09-28 | Adds explicit specification governance, preserves accepted decisions through ADR supersession, and establishes MCP as the preferred future agent-integration boundary with external AI orchestration | `docs/versions/spec-v0.2.0.md` |

## Rules

- Do not overwrite historical decisions in place when their meaning changes. Create a new ADR and mark the older ADR as superseded through metadata/indexing.
- Requirement IDs are stable. A materially changed requirement receives a new ID and explicitly supersedes the old one.
- Every material planning change must name the spec version in which it was introduced.
- The current baseline is described by the latest version manifest plus all inherited, non-superseded decisions from earlier baselines.
- Git history remains the exact byte-level history; version manifests make that history understandable without reconstructing intent from commits alone.

See `docs/governance/VERSIONING.md` for the complete policy.