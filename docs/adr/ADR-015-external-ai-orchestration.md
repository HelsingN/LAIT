# ADR-015: External AI Orchestration

- **Status:** Accepted
- **Date:** 2026-09-28
- **Spec version introduced:** 0.2.0
- **Decision owners:** Project owner
- **Supersedes:** None
- **Superseded by:** None
- **Related requirements:** MODL-12, INTG-01, existing AI-feature/provider requirements

## Context

LAIT already distinguishes AI providers from AI features. Provider modules answer how a model is called; feature modules answer why it is called for a bounded learning task such as chunk extraction, semantic evaluation, or exercise generation.

A future AI tutor can add another layer: deciding what the learner should do next, how much scaffolding to provide, when to switch exercise type, when to move into free speaking, and how to combine LAIT learning state with broader conversational context.

Embedding that open-ended conversational strategy directly into the LAIT core would couple persistent learning state to one orchestration implementation and make the core harder to reason about, test, and reuse.

## Decision

Treat open-ended AI tutoring/conversation strategy as an optional external orchestration layer.

LAIT remains the authoritative learning engine and durable learning-state owner. External agent frameworks, including a possible DeepSeek Harness integration, may orchestrate sessions by reading state and invoking documented LAIT use cases through MCP or another public adapter.

### LAIT owns

- Lesson and SourceRevision identity/provenance;
- LearningUnit identity and evidence;
- Exercise definitions and instances;
- Attempt persistence;
- Evaluation records and corrections/overrides;
- weak-unit evidence;
- review scheduling inputs/outcomes;
- durable jobs and persistent learning state;
- bounded AI features used by those workflows.

### External orchestration may own

- conversational flow;
- deciding which available learning activity to request next;
- deciding when to reduce or increase scaffolding;
- combining LAIT evidence with wider agent context;
- guiding interview practice and free-speaking interactions;
- requesting LAIT to persist resulting attempts/evidence.

The external orchestrator must not become the only source of truth for learning progress.

## Internal AI versus orchestration AI

These remain distinct concepts.

### Bounded/internal AI feature

Examples:

- extract candidate lexical chunks;
- semantically evaluate an answer;
- generate an exercise payload;
- produce a concise feedback explanation.

These remain LAIT application/module capabilities with explicit schemas, prompts/rubrics, traceability, and provider abstraction.

### External orchestration

Examples:

- choose whether the next activity should be Gap Fill or free production;
- decide whether to revisit a weak preposition after two successful attempts;
- run a 15-minute interview-practice conversation using due-review evidence;
- decide when to ask for a self-generated paraphrase rather than another source reconstruction.

This layer may be implemented by DeepSeek Harness or another compatible agent client.

## Alternatives considered

### Put the tutor agent loop inside LAIT Core

Rejected because agent strategy is more volatile than the durable learning model and would create strong coupling between persistence/invariants and a specific orchestration style.

### Remove AI features from LAIT and delegate every AI call to an external agent

Rejected because bounded features such as source analysis and evaluation are part of the product's reliable learning workflow and require consistent schemas, auditability, retries, and provider abstraction.

### Treat DeepSeek Harness as the only supported orchestrator

Rejected because the architecture should preserve client portability. DeepSeek Harness is a strong candidate and reference integration, not a mandatory platform dependency.

## Consequences

### Positive

- Persistent pedagogical state remains deterministic and auditable.
- Agent frameworks can evolve independently from LAIT's domain model.
- The same LAIT engine can serve Web UI, MCP clients, CLI tools, and future clients.
- DeepSeek Harness can contribute rich reasoning, conversation, tools, and context without owning the learning database.
- Internal AI features remain testable with deterministic fake providers.

### Negative

- Some decisions about session flow may exist outside LAIT, so the boundary between orchestration state and durable learning evidence must be explicit.
- A useful external tutor requires a sufficiently expressive read/write integration surface.
- Cross-system tracing will eventually need correlation/session identifiers.

### Risks

- If too much pedagogical policy is moved outside LAIT, different orchestrators may produce inconsistent learning behavior.
- If too much orchestration logic is moved back into Core, the separation loses value.
- Persisting agent conversation history as if it were learning evidence could pollute review state unless attempt/evidence contracts remain strict.

## Guardrails

- Only validated LAIT commands may mutate learning state.
- External agents may recommend or request actions; Core/application invariants remain authoritative.
- Review scheduling must derive from persisted evidence, not opaque agent memory.
- AI orchestration context is not automatically a domain record.
- If an external session needs persistence, define an explicit application/domain contract rather than storing arbitrary agent state in core tables.

## Deferred design questions

- whether `PracticeSession` becomes a first-class core entity;
- which orchestration decisions should be persisted for audit/replay;
- how agent-generated free-speaking evidence maps to Attempts;
- how to version a pedagogical orchestration policy if LAIT later ships its own agent;
- correlation IDs and tracing across MCP and LAIT jobs.

These require separate ADRs once concrete implementation use cases exist.

## Validation

The decision is validated when an external agent can conduct a meaningful practice interaction while:

- using LAIT as the source of truth for learning state;
- persisting attempts/evidence through public use cases;
- replacing the agent framework without migrating core learning records;
- leaving bounded internal AI features independently testable and usable without the agent framework.

## Related documents

- `docs/adr/ADR-014-external-integration-boundary-and-mcp.md`
- `docs/versions/spec-v0.2.0.md`
- `.planning/research/ARCHITECTURE.md`
- `.planning/REQUIREMENTS.md`
