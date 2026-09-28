# LAIT Specification Baseline 0.2.0

**Status:** Current planning baseline
**Date:** 2026-09-28
**Inherits:** `0.1.0`

## Summary

Version 0.2.0 preserves the existing small-core Mod-First architecture and v1 delivery scope while adding explicit planning governance and a clearer long-term AI integration model.

The central new architectural direction is:

> LAIT remains the authoritative learning engine and durable learning-state owner. External agent frameworks may act as AI orchestration layers through a stable application boundary, with MCP as the preferred future generic integration adapter.

## Decisions introduced

### ADR-013 — Specification and decision versioning

Planning baselines, ADRs, and requirement changes are now explicitly versioned. Accepted decisions are not silently rewritten when meaning changes; new ADRs supersede old ones.

### ADR-014 — External integration boundary and MCP

LAIT must remain usable through application-level use cases independent of React, FastAPI transport details, or a specific agent framework. MCP is the preferred future agent integration adapter, but is not a v1 implementation dependency.

### ADR-015 — External AI orchestration

Conversation strategy and dynamic tutoring orchestration may live in an external agent framework such as DeepSeek Harness. LAIT keeps responsibility for learning identity/state, exercises, attempts, evaluations, review evidence, scheduling, and persistence.

## Architectural delta from 0.1.0

The previous flow:

```text
React UI
  -> FastAPI
  -> Application Layer
  -> Core / Modules / Persistence
```

remains valid, but is generalized to:

```text
                   +-------------------+
                   | React Web Client  |
                   +---------+---------+
                             |
                   +---------v---------+
                   | HTTP/FastAPI      |
                   | Adapter           |
                   +---------+---------+
                             |
+-------------------+        |
| External AI Agent |        |
| / DeepSeek Harness|        |
+---------+---------+        |
          | MCP              |
+---------v---------+        |
| MCP Adapter       |        |
+---------+---------+        |
          |                  |
          +--------+---------+
                   |
          +--------v---------+
          | Application      |
          | Use Cases        |
          +--------+---------+
                   |
          +--------v---------+
          | LAIT Core        |
          | + Modules        |
          | + Persistence    |
          +------------------+
```

The important property is that HTTP and MCP are peer adapters over the same application use cases.

## Responsibility split

### LAIT owns

- Lesson and SourceRevision identity;
- LearningUnit identity, provenance, and learning evidence;
- Exercise definitions/instances;
- Attempt history;
- Evaluation records;
- weak-unit evidence and due-review state;
- scheduler inputs/outcomes;
- durable jobs and domain persistence;
- narrow AI features such as extraction, semantic evaluation, or exercise generation when configured.

### External AI orchestration may own

- conversational teaching strategy;
- deciding which learning activity to request next;
- deciding when to increase/decrease scaffolding;
- combining LAIT state with wider agent context;
- running a guided interview-practice or free-speaking interaction;
- calling LAIT tools/resources to persist the resulting learning evidence.

The external orchestrator must not become the source of truth for learning state.

## MCP direction

A future MCP adapter should expose domain-oriented capabilities, not UI automation.

Likely tool/resource families include:

- lessons and sources;
- learning units;
- practice/exercise generation;
- attempts and evaluation submission;
- due reviews and learning evidence;
- progress/context reads.

Examples such as `create_lesson`, `get_due_reviews`, `generate_exercise`, and `submit_attempt` are directional names only. Exact MCP v1 contracts remain deferred until the first working vertical learning slice proves the application use cases.

## Scope impact

### v1

No additional v1 feature is introduced. The existing Phase 1–9 roadmap remains authoritative for delivery sequencing.

Production MCP remains out of v1, consistent with existing requirements.

### Post-v1 / integration work

After a working vertical slice exists, a small MCP spike should validate that an external client can execute a complete learning loop through public application boundaries without accessing private storage or UI internals.

## Deferred design questions

These are deliberately not fixed by 0.2.0:

- exact MCP tool/resource names and schemas;
- whether MCP is served in-process, by the FastAPI process, or by a dedicated adapter process;
- DeepSeek Harness packaging/distribution details;
- whether `PracticeSession` becomes a first-class core entity or remains an application-level aggregate/workflow;
- streaming/subscription behavior for long-running jobs over MCP;
- authentication/authorization for remote rather than local MCP use.

These require separate ADRs when implementation pressure makes them concrete.

## Validation criteria

This direction is validated when a future integration can:

1. create/read learning state through documented application interfaces;
2. generate or request practice;
3. submit an attempt;
4. receive/persist evaluation and review evidence;
5. do so without importing private LAIT modules or reading/writing database tables directly;
6. leave the normal React/FastAPI client behavior unchanged.

## Historical trace

The inherited pre-change baseline is `docs/versions/spec-v0.1.0.md`, anchored at commit `9c5a2c7c9a31ea84de280779ce12dcc3a2e0436b`.