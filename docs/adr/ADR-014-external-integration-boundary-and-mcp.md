# ADR-014: External Integration Boundary and MCP

- **Status:** Accepted
- **Date:** 2026-09-28
- **Spec version introduced:** 0.2.0
- **Decision owners:** Project owner
- **Supersedes:** None
- **Superseded by:** None
- **Related requirements:** MODL-12, INTG-01

## Context

LAIT is designed as a standalone learning application, but future integrations may include AI agent frameworks, CLI clients, desktop/mobile clients, and other tools. DeepSeek Harness is one concrete candidate, but coupling LAIT to one agent runtime would reduce portability and could force a rewrite if the integration strategy changes.

The existing architecture already separates FastAPI transport from the application/domain layers and explicitly preserves a future MCP adapter boundary. The new requirement is to make that boundary a deliberate architectural direction rather than an incidental possibility.

## Decision

LAIT remains a standalone, headless-capable domain application whose canonical behavior is exposed through application-level use cases.

1. React is a client, not the semantic center of LAIT.
2. FastAPI is an HTTP adapter/composition surface, not the owner of business logic.
3. Application use cases must be callable independently of HTTP and UI adapters.
4. Stable domain/application IDs must be usable by non-UI clients.
5. Long-running operations must expose durable job identity/state rather than rely on one request lifetime.
6. Future integrations must use documented application commands/queries and must not read or mutate private database tables.
7. MCP is the preferred future generic agent-integration adapter.
8. MCP implementation is deferred until a working vertical learning slice exists; it is not a Phase 1 dependency and does not expand v1 scope.
9. DeepSeek Harness, if integrated, should consume the MCP/application boundary rather than become a dependency of the LAIT core.

Conceptually:

```text
React Web -> HTTP/FastAPI -+
                          |
External Agent -> MCP ----+-> Application Use Cases -> Core/Modules/Persistence
```

HTTP and MCP are peer adapters over the same application behavior.

## MCP surface principle

Future MCP capabilities should expose domain semantics, not UI automation.

Preferred direction:

- lesson/source operations;
- learning-unit queries and mutation;
- practice/exercise generation;
- attempt submission and evaluation state;
- due-review and learning-evidence queries;
- progress/context reads.

Avoid MCP tools such as `click_next_button`, `open_tab`, or other UI-specific actions.

Exact tool/resource names, schemas, streaming behavior, and process topology are intentionally deferred to a later ADR.

## Alternatives considered

### Make DeepSeek Harness the primary runtime now

Rejected because LAIT's learning engine should remain independently usable and the current v1 scope does not require an agent harness.

### Build MCP immediately in Phase 1

Rejected because MCP would add integration work before the core vertical learning loop has proven the use cases it should expose.

### Expose only the HTTP API and let every integration depend on transport DTOs

Not selected as the architectural rule. HTTP remains useful, but application use cases should exist below transport so future adapters do not need to emulate a browser client or inherit accidental HTTP-specific semantics.

### Direct database integration

Rejected because it bypasses invariants, migrations, permissions, and future compatibility contracts.

## Consequences

### Positive

- LAIT can remain a standalone product.
- DeepSeek Harness becomes one optional client/orchestrator rather than a platform dependency.
- MCP can later support multiple AI clients, not only DeepSeek.
- Application boundaries become easier to test without a browser or HTTP server.
- The architecture gains a concrete portability test.

### Negative

- Application contracts must be designed deliberately rather than letting routers own workflows.
- Stable IDs and job semantics need attention earlier.
- A future MCP adapter will require its own schema/version governance.

### Risks

- Over-designing a future MCP contract before real use cases exist.
- Accidentally allowing UI assumptions to leak into application use cases.
- Duplicating behavior between HTTP and MCP rather than sharing application handlers.

## Validation

After the first working vertical slice, a small MCP spike should be able to perform a complete learning loop without UI automation or private storage access:

1. create/read lesson state;
2. create/read learning units;
3. request/generate practice;
4. submit an attempt;
5. receive/persist evaluation/review evidence.

Failure to do this without special-case core changes is evidence that the application boundary is too tightly coupled to the Web/API adapters.

## Related documents

- `docs/versions/spec-v0.2.0.md`
- `docs/adr/ADR-015-external-ai-orchestration.md`
- `.planning/REQUIREMENTS.md` (`MODL-12`, `INTG-01`)
- `.planning/research/ARCHITECTURE.md`
