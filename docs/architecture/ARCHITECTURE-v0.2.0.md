# LAIT Architecture — Specification 0.2.0 Overlay

**Status:** Current architecture overlay
**Date:** 2026-09-28
**Inherits:** `.planning/research/ARCHITECTURE.md` and specification baseline `0.1.0`

## Purpose

This document does not replace the original architecture research. It records only the architectural additions accepted in specification `0.2.0` so older reasoning remains visible.

## Unchanged foundation

LAIT remains a small-core, Mod-First modular monolith with:

- React/TypeScript as the initial Web client;
- FastAPI as transport/composition adapter;
- application commands/queries above a framework-independent domain core;
- static trusted bundled modules for the MVP;
- narrow typed extension contracts;
- deterministic-first evaluation;
- durable job state for long-running AI work;
- SQLite local persistence with a future PostgreSQL adapter path.

## New integration perspective

The system is now explicitly treated as headless-capable. The Web UI and HTTP API are not the only possible clients.

```text
                         +----------------------+
                         | React Web Client     |
                         +----------+-----------+
                                    |
                              HTTP / OpenAPI
                                    |
                         +----------v-----------+
                         | FastAPI Adapter      |
                         +----------+-----------+
                                    |
                                    |
+----------------------+            |
| External AI Agent    |            |
| e.g. DeepSeek Harness|            |
+----------+-----------+            |
           | MCP                    |
+----------v-----------+            |
| MCP Adapter          |            |
+----------+-----------+            |
           |                        |
           +-----------+------------+
                       |
              +--------v---------+
              | Application      |
              | Use Cases        |
              +--------+---------+
                       |
              +--------v---------+
              | Core Kernel      |
              | + Module Host    |
              +--------+---------+
                       |
              +--------v---------+
              | Persistence /    |
              | Durable Jobs     |
              +------------------+
```

## Adapter rule

All external clients should invoke the same application semantics.

Good boundary:

```text
HTTP adapter -> CreateLesson handler
MCP adapter  -> CreateLesson handler
CLI adapter  -> CreateLesson handler
```

Bad boundary:

```text
MCP adapter -> HTTP route implementation -> business logic
```

Business logic must not be duplicated across adapters.

## External AI orchestration

LAIT does not require a general-purpose agent loop in Core.

LAIT owns durable learning state and bounded learning operations. An external orchestrator may decide which learning activity to request next and conduct a conversation around those operations.

This separates:

```text
LAIT learning engine
- identity
- provenance
- attempts
- evaluation
- review evidence
- scheduling
- persistence
- bounded AI features

from

External orchestration
- conversation strategy
- activity sequencing
- dynamic scaffolding
- interview/free-speaking flow
- broader agent context
```

## MCP role

MCP is the preferred future generic integration adapter for agent frameworks. It is intentionally deferred until the first end-to-end learning slice exists.

The future MCP surface should expose domain-oriented capabilities such as lessons, learning units, practice, attempts, evaluation state, due reviews, and progress. It should not expose Web UI mechanics.

## Compatibility requirements created by this direction

Current implementation work should preserve these properties even before MCP exists:

1. application use cases are callable without React or an HTTP request object;
2. domain IDs are stable and transport-neutral;
3. durable jobs have stable identifiers and observable state;
4. integrations do not require direct database access;
5. capability/module discovery can be represented in machine-readable form;
6. external orchestration cannot bypass core/application invariants when recording learning evidence.

## Deferred decisions

This overlay does not decide:

- exact MCP tool/resource schemas;
- MCP transport/process topology;
- DeepSeek Harness plugin package design;
- runtime plugin installation for LAIT;
- whether PracticeSession becomes a first-class core entity;
- agent-session persistence or replay semantics.

Those remain future ADRs.

## Governing ADRs

- `ADR-013-specification-and-decision-versioning.md`
- `ADR-014-external-integration-boundary-and-mcp.md`
- `ADR-015-external-ai-orchestration.md`
