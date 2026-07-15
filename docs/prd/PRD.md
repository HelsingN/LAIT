# AI Language Coach — Product Requirements Document

**Document:** `PRD.md`  
**Version:** 1.0-prealpha  
**Status:** Pre-Alpha Architecture Baseline  
**Product stage:** MVP discovery and planning  
**Primary platform:** Responsive Web Application  
**Architecture strategy:** Small Core + Mod-First Extension Architecture

---

## 1. Executive Summary

AI Language Coach is an AI-powered learning application designed to help adult language learners convert passive knowledge into active speaking ability.

The first target audience is adult IT professionals with approximately B1–B2 English who want to prepare for interviews, activate professional vocabulary, and become more fluent when speaking about their experience.

The application uses retrieval practice, lexical chunks, progressive removal of prompts, semantic evaluation of free-form answers, spaced repetition of weak material, and user-controlled AI assistance.

Unlike conventional flashcards and basic gap-fill exercises, the product progressively reduces support until the learner can reconstruct a sentence, paragraph, or idea from memory and produce a natural answer independently.

The MVP will be intentionally small, but its architecture must support incremental expansion through independently developed modules. New exercise types, languages, importers, AI capabilities, providers, schedulers, integrations, and MCP adapters must be addable without modifying the core domain logic.

This document is the primary product input for GSD. It defines product intent, scope, architectural constraints, module boundaries, risks, acceptance criteria, and unresolved questions. Detailed API schemas, database structures, UI specifications, implementation tasks, and deployment architecture should be derived during the GSD research and planning stages.

---

## 2. Problem Statement

Many intermediate and upper-intermediate language learners understand substantially more than they can produce.

Typical problems include:

- a large passive vocabulary but a limited active vocabulary;
- difficulty retrieving familiar words and structures under speaking pressure;
- memorization of isolated words instead of reusable lexical chunks;
- excessive reliance on recognition exercises;
- weak retention of prepositions, linking words, auxiliary verbs, articles, and word order;
- difficulty producing natural professional answers during interviews;
- limited feedback on valid paraphrases and free-form responses;
- lack of systematic recycling of repeated mistakes.

Existing tools solve only parts of the problem:

- **Anki** is strong at spaced repetition but is usually card-oriented and depends on manually prepared material.
- **NotebookLM** is strong at source-grounded understanding but is not optimized for structured active recall.
- **General-purpose AI assistants** can generate exercises and explanations but typically do not maintain a persistent learning model, a review queue, or stable exercise workflows.
- **Traditional learning applications** often prioritize recognition, gamification, or fixed curricula rather than user-owned professional content.

The product opportunity is to combine user-owned source material, lexical and structural analysis, progressive retrieval exercises, deterministic and semantic answer evaluation, persistent tracking of weak chunks, adaptive review, and an extension architecture that enables new learning methods without rebuilding the application.

---

## 3. Product Vision

Build a personal, extensible AI Language Coach that continuously transforms authentic user material into structured active-recall practice and adapts future exercises to the learner's actual difficulties.

Long-term, the product should become a modular learning platform where official developers and community developers can add capabilities through the same documented extension contracts.

---


## 3.1 Product Evolution Philosophy

AI Language Coach is intentionally designed as an evolving learning platform rather than a fixed application.

The MVP implements only one complete learning workflow while keeping the Core intentionally small.

Every future capability—including exercise types, languages, AI features, review algorithms, importers, exporters, integrations, clients, and MCP adapters—should be implemented as an independent module whenever practical.

The architecture favors continuous incremental evolution over periodic rewrites.

Core responsibilities should change slowly. Most innovation should happen inside replaceable modules.

**Guiding principle**

> Design for runtime extensibility. Implement build-time extensibility first.

---

## 4. Product Goals

### 4.1 MVP goals

The MVP must prove that a learner can:

1. paste authentic text;
2. extract and review useful lexical chunks;
3. generate a small set of retrieval-based exercises;
4. complete exercises with progressively reduced support;
5. receive reliable feedback;
6. save mistakes and weak learning units;
7. review weak material later;
8. use the complete flow on desktop and mobile browsers.

### 4.2 Architectural goals

The MVP must also validate that:

- exercise types can be added as modules;
- language-specific behavior can be added as modules;
- AI providers are replaceable;
- AI features are separate from AI providers;
- modules communicate through public contracts rather than private imports;
- official modules use the same extension interfaces intended for future community modules;
- MCP and external integrations can be implemented as adapters without becoming core dependencies.

### 4.3 Non-goals

The first version is not intended to:

- become a full language-learning ecosystem;
- replace a teacher;
- support every language;
- provide a plugin marketplace;
- run untrusted third-party code;
- offer advanced pronunciation coaching;
- provide complete offline AI execution;
- implement enterprise multi-tenancy.

---

## 5. Target Audience

### 5.1 Primary persona

An adult IT professional who:

- has English around B1–B2;
- understands technical texts and interviews reasonably well;
- struggles to produce fluent, structured answers;
- wants to prepare self-introductions, interview stories, and technical explanations;
- prefers using their own professional material;
- is comfortable with a web application;
- wants concise feedback rather than long grammar lectures.

### 5.2 Secondary audiences

Future versions may support general English learners, learners of other languages, speaking clubs, teachers and tutors, corporate training, exam preparation, and professional communication outside IT.

The MVP should remain optimized for the primary persona.

---

## 6. Core Learning Method

The central learning method is progressive retrieval.

### 6.1 Learning sequence

A source sentence may move through the following stages:

1. **Recognition** — select or insert a missing target word.
2. **Chunk completion** — restore a preposition, auxiliary, collocation, or phrase.
3. **Sentence reconstruction** — rebuild the full sentence from fragments.
4. **Keyword recall** — reconstruct the sentence using only semantic anchors.
5. **Paragraph recall** — restore a connected passage from a small set of prompts.
6. **Free production** — express the same idea naturally without reproducing the original wording exactly.

### 6.2 Learning principles

1. **Active recall over recognition**
2. **Chunks over isolated words**
3. **Meaning over exact memorization**
4. **Progressive difficulty**
5. **User control over AI output**
6. **Short actionable feedback**
7. **Recycling of weak material**

---

## 7. Core User Workflow

```text
Create lesson
→ Paste source text
→ Select source and target language
→ Analyze source
→ Review extracted learning units
→ Generate exercises
→ Complete exercises
→ Receive deterministic or AI-assisted feedback
→ Save attempts and weak units
→ Add weak units to review queue
→ Review later
```

---

## 8. Product Scope

### 8.1 MVP — Included

#### Lesson management

- Create, rename, edit, archive, and delete a lesson.
- Paste plain text.
- Store original source text.
- Select a supported language.
- Preserve source text separately from generated content.

#### Learning-unit analysis

- Extract lexical chunks.
- Extract collocations.
- Extract phrasal verbs.
- Extract useful sentence patterns.
- Optionally identify relevant grammar structures.
- Show where each unit occurs in the source.
- Allow accept, edit, reject, and manually add operations.

#### Exercise generation

The MVP must support at least these bundled exercise modules:

1. Gap Fill
2. Chunk Completion
3. Sentence Reconstruction
4. Keyword Recall

Paragraph Recall may be included if it does not jeopardize the MVP schedule.

#### Exercise sessions

- Start a session from a lesson.
- Display one exercise at a time.
- Submit answers.
- Show feedback.
- Continue, retry, or reveal the source.
- Save attempt history.

#### Evaluation

- Deterministic validation for closed exercises.
- Normalized text comparison where appropriate.
- AI semantic evaluation for open answers.
- Clear distinction between correct, acceptable paraphrase, partially correct, incorrect, and unable to evaluate reliably.

#### Progress and review

- Track attempts.
- Track weak learning units.
- Track recent success/failure.
- Create a review queue.
- Use a simple replaceable scheduling strategy.
- Allow the learner to mark an item manually as easy, difficult, or mastered.

#### Platform

- Responsive web application.
- Desktop-browser usability.
- Mobile-browser usability.
- Docker Compose local deployment.
- Single-user mode for the initial MVP.

### 8.2 MVP — Explicitly Excluded

- Native iOS or Android application.
- Desktop application.
- Public plugin marketplace.
- Runtime installation of arbitrary third-party code.
- Third-party plugin sandboxing.
- Full role and permission system for multiple users.
- Teacher or classroom dashboards.
- Team collaboration.
- Payments and subscriptions.
- PDF, DOCX, web page, or YouTube import.
- Advanced pronunciation scoring.
- Local Whisper.
- Local LLM execution.
- Speech synthesis.
- Complex gamification.
- Social features.
- Public lesson sharing.
- Full Anki integration.
- NotebookLM integration.
- Production MCP server or MCP client.
- Enterprise authentication.
- Multi-tenant SaaS infrastructure.

---

## 9. Mod-First Architecture

### 9.1 Architectural direction

The product will use a:

> **Modular Monolith with a Small Core and a Mod-First Extension Architecture**

The system should be designed for runtime extensibility, but the MVP will implement build-time extensibility first.

This means:

- one deployable backend;
- one main database;
- one responsive frontend;
- clearly separated modules;
- explicit public contracts;
- statically bundled trusted modules;
- no marketplace or untrusted runtime plugins in the MVP.

### Governing rule

> Design for runtime extensibility; implement build-time extensibility first.

### 9.2 Architectural principles

1. The core must remain small and domain-focused.
2. New exercise types must be addable without modifying core domain logic.
3. New languages must be addable through language modules.
4. AI providers and AI-powered features must be separate extension categories.
5. Official and future community modules must use the same public extension contracts.
6. Modules communicate through documented interfaces, capabilities, commands, and events.
7. The MVP uses statically bundled trusted modules.
8. Runtime installation, sandboxing, signatures, and marketplace support are deferred.
9. MCP is an adapter over the application API, not a core dependency.
10. Modules must be independently testable.
11. Core data remains stable; module-specific data belongs to module-owned storage.
12. Plugin and extension API compatibility must be versioned explicitly.
13. No bundled module may rely on undocumented privileged access.
14. Direct cross-module imports should be avoided except through shared SDK contracts.
15. Architecture complexity must not prevent delivery of the learning workflow.

### 9.3 Logical architecture

```text
┌─────────────────────────────────────────────────┐
│                  Client Layer                   │
│          Web UI / Future PWA / Mobile           │
├─────────────────────────────────────────────────┤
│                Extension Modules                │
│ Exercises · Languages · AI · Imports · MCP      │
├─────────────────────────────────────────────────┤
│              Public Extension API               │
│ Capabilities · Commands · Events · Storage      │
├─────────────────────────────────────────────────┤
│                  Core Kernel                    │
│ Lessons · Units · Attempts · Reviews · Host     │
├─────────────────────────────────────────────────┤
│               Infrastructure Layer              │
│ Database · LLM transport · HTTP · File storage  │
└─────────────────────────────────────────────────┘
```

### 9.4 Core responsibilities

The core should contain only capabilities required by all learning workflows.

#### Core domain entities

- Lesson
- SourceContent
- LearningUnit
- ExerciseDefinition
- ExerciseInstance
- ExerciseAttempt
- EvaluationResult
- ReviewItem
- ModuleManifest
- Capability
- Command
- DomainEvent

#### Core services

- **Lesson Service** — lesson lifecycle, source storage, lesson metadata.
- **Learning Unit Registry** — registration and storage of typed learning units.
- **Exercise Registry** — discovery and dispatch for exercise modules.
- **Attempt Service** — answer submission, persistence, and result association.
- **Review Service** — due items, scheduling requests, and review outcomes.
- **Module Host** — static module registration, validation, activation, and capability registration.

The Lesson Service must not contain chunk extraction logic. The core must not hard-code the behavior of individual exercise types.

### 9.5 Extension categories

#### Exercise modules

Examples:

- `exercise-gap-fill`
- `exercise-chunk-completion`
- `exercise-sentence-reconstruction`
- `exercise-keyword-recall`
- future `exercise-dictation`
- future `exercise-shadowing`
- future `exercise-interview-simulation`

#### Language modules

Examples:

- `language-en`
- future `language-he`
- future `language-es`

A language module may provide tokenization, normalization, punctuation handling, stop words, morphology helpers, directionality metadata, and language-specific prompts.

The core must not assume that all languages use Latin script or left-to-right layout.

#### AI provider modules

Examples:

- `ai-provider-openai-compatible`
- future `ai-provider-gemini`
- future `ai-provider-ollama`

Possible provider capabilities include text generation, structured generation, embeddings, semantic evaluation, speech-to-text, and text-to-speech.

#### AI feature modules

Examples:

- `ai-feature-chunk-extractor`
- `ai-feature-exercise-generator`
- `ai-feature-semantic-evaluator`
- future `ai-feature-difficulty-estimator`
- future `ai-feature-interview-roleplay`

Rule:

```text
AI Provider = how a model is called
AI Feature  = why a model is called
```

#### Importer modules

MVP: `import-plain-text`

Future: Markdown, PDF, DOCX, subtitles, YouTube transcript, web page, Obsidian note.

#### Exporter modules

Future: Markdown, JSON, CSV, Anki, Obsidian.

#### Scheduler modules

MVP: simple scheduler.

Future: SM-2, FSRS, adaptive personalized scheduler.

#### MCP and integration modules

MCP must consume documented application commands and services rather than internal database structures.

### 9.6 Capability-based dependency model

Modules should depend on capabilities rather than concrete implementations.

```python
provider = capability_registry.resolve("ai.structured_generation")
```

This enables provider replacement, local/cloud fallback, user selection, and future capability routing.

### 9.7 Commands and events

Initial commands may include:

- `lesson.create`
- `lesson.update`
- `lesson.analyze`
- `learning_unit.accept`
- `learning_unit.reject`
- `exercise.generate`
- `exercise.submit`
- `review.start`

Initial events may include:

- `lesson.created`
- `lesson.updated`
- `analysis.completed`
- `learning_unit.created`
- `exercise.generated`
- `attempt.submitted`
- `attempt.evaluated`
- `review.scheduled`
- `module.activated`

The MVP may use an in-process event bus. A distributed broker is not required.

### 9.8 Module manifest

Every bundled module should declare a manifest even if modules are statically compiled.

```yaml
id: official.exercise.gap-fill
name: Gap Fill
version: 0.1.0
apiVersion: 1
publisher: ai-language-coach
category: exercise

capabilities:
  - exercise.generate
  - exercise.evaluate

permissions:
  - lesson.read
  - learning-unit.read
  - attempt.write

dependencies:
  - core.exercise-api >=0.1.0

entrypoints:
  backend: plugin.py
  frontend: index.ts
```

The exact schema will be finalized during GSD architecture planning.

### 9.9 Module data and storage

The system should distinguish:

- **Core-owned data** — lessons, source content, learning units, attempts, evaluations, reviews, module registration.
- **Module-owned relational data** — complex feature-specific data.
- **Module settings/document storage** — prompt templates, model parameters, UI preferences, and small module state.

Modules must not modify another module's private storage directly.

### 9.10 Security and trust model

#### MVP

- only bundled modules;
- all modules reside in the primary repository;
- all modules are trusted;
- static registration;
- no arbitrary package execution;
- no marketplace;
- no sandbox.

#### Future

- local plugin installation;
- permission review;
- signed packages;
- trust levels;
- compatibility validation;
- marketplace;
- sandboxing.

A permission vocabulary may be defined early, but enforcement beyond bundled modules is not an MVP requirement.

### 9.11 Frontend extensibility

The frontend should support module registration for exercise renderers, editors, routes, settings panels, sidebar items, widgets, commands, and context actions.

For the MVP, frontend modules will be bundled at build time. Dynamic JavaScript loading is not required.

### 9.12 Recommended architectural style

- modular monolith;
- hexagonal architecture;
- dependency inversion;
- capability registry;
- command bus;
- domain/application events;
- build-time bundled modules;
- shared Python and TypeScript contracts.

Microservices are explicitly not required for the MVP.

---

## 10. Initial Bundled Modules

### Core and platform

- core lesson domain;
- learning-unit registry;
- exercise registry;
- attempt service;
- review service;
- static module host;
- capability registry;
- command bus;
- event bus.

### Official bundled modules

- `language-en`
- `import-plain-text`
- `learning-unit-lexical-chunk`
- `exercise-gap-fill`
- `exercise-chunk-completion`
- `exercise-sentence-reconstruction`
- `exercise-keyword-recall`
- `ai-provider-openai-compatible`
- `ai-feature-chunk-extractor`
- `ai-feature-semantic-evaluator`
- `scheduler-simple`

---

## 11. Functional Requirements

- **FR-001** Create a lesson from pasted text.
- **FR-002** Preserve the original source.
- **FR-003** Extract candidate learning units.
- **FR-004** Accept, edit, reject, and manually add learning units.
- **FR-005** Discover available exercise modules through the registry.
- **FR-006** Generate exercises from accepted units.
- **FR-007** Use deterministic evaluation where feasible.
- **FR-008** Use replaceable semantic AI evaluation for open answers.
- **FR-009** Show submitted answer, reference, result category, concise explanation, and optional natural alternative.
- **FR-010** Persist every submitted attempt.
- **FR-011** Track weak learning units.
- **FR-012** Generate a due-review queue.
- **FR-013** Register bundled modules through documented interfaces.
- **FR-014** Keep vendor-specific AI SDKs inside provider adapters.
- **FR-015** Receive language capabilities through language modules.
- **FR-016** Support desktop and mobile browser widths.

---

## 12. Non-Functional Requirements

- **NFR-001 Modularity:** add an exercise module without changing core domain logic.
- **NFR-002 Testability:** core services and modules are independently testable.
- **NFR-003 Local deployment:** application runs through Docker Compose.
- **NFR-004 Unicode:** preserve multilingual UTF-8 text correctly.
- **NFR-005 Reliability:** failed AI requests do not corrupt lesson or attempt data.
- **NFR-006 AI traceability:** store provider, model, feature, prompt version, and timestamp.
- **NFR-007 Cost awareness:** measure AI usage by feature and request.
- **NFR-008 Versioning:** public extension contracts have explicit API versions.
- **NFR-009 Security:** secrets are not stored in source code or exposed to the frontend.
- **NFR-010 Graceful degradation:** lessons and review data remain available when AI is unavailable.
- **NFR-011 Performance:** normal analysis and generation tasks do not freeze the UI.
- **NFR-012 Portability:** avoid opaque vendor-only storage.

---

## 13. Technology Constraints

### Frontend

- React
- TypeScript
- responsive web UI

### Backend

- Python
- FastAPI
- modular monolith

### Database

- SQLite for MVP
- migration path to PostgreSQL

### Deployment

- Docker
- Docker Compose

### AI

- provider abstraction;
- initial OpenAI-compatible provider;
- structured outputs where possible;
- no core dependency on a specific vendor.

### Future clients

- PWA;
- mobile companion;
- Tauri desktop edition.

Precise framework versions, repository strategy, ORM, background jobs, and package boundaries should be selected during GSD research.

---

## 14. User Stories

- **US-001:** As a learner, I want to paste my own professional text.
- **US-002:** As a learner, I want the system to extract reusable chunks.
- **US-003:** As a learner, I want to review and edit extracted chunks.
- **US-004:** As a learner, I want progressively harder exercise types.
- **US-005:** As a learner, I want natural paraphrases to be accepted.
- **US-006:** As a learner, I want mistakes linked to specific chunks.
- **US-007:** As a learner, I want difficult chunks to return later.
- **US-008:** As a developer, I want to add an exercise type through a public contract.
- **US-009:** As a developer, I want to add a language module.
- **US-010:** As a developer, I want to add or replace an AI provider.
- **US-011:** As an integration developer, I want to expose application commands through MCP without direct storage access.

---

## 15. Evaluation Strategy

### 15.1 Deterministic evaluation

Use deterministic rules for selected options, exact missing words, normalized chunk completion, known token ordering, and predefined accepted variants.

Normalization may include whitespace, capitalization, punctuation tolerance, contractions, and language-specific rules.

### 15.2 AI-assisted evaluation

Use semantic evaluation for sentence reconstruction with paraphrasing, keyword recall, paragraph recall, and free production.

Expected structured result:

```yaml
status: correct | acceptable | partial | incorrect | uncertain
meaning_preserved: true
grammar_ok: true
target_chunks_used:
  - be responsible for
missing_or_weak:
  - current role
feedback: "Your answer is clear. Use 'responsible for' rather than 'responsible to'."
natural_alternative: "I'm responsible for maintaining Linux-based test systems."
```

When confidence is low, the evaluator must return `uncertain`.

---

## 16. Review and Scheduling Strategy

The MVP should use a simple replaceable scheduler module based on recent correctness, failure count, learner difficulty rating, and time since last review.

The exact algorithm remains open for GSD research.

---

## 17. Data Ownership and Privacy Principles

- User content belongs to the user.
- Source text must not be silently modified.
- AI provider transmission must be disclosed.
- Secrets must be stored securely.
- Unnecessary personal information should not be sent to AI providers.
- Deletion behavior must be defined.
- A local-first deployment path should remain possible.

---

## 18. Success Metrics

- A user can create and analyze a lesson without technical assistance.
- A complete exercise set can be generated in under five minutes for a normal lesson.
- At least 80% of generated exercises are usable after learning-unit review.
- The full workflow works without manual database or configuration edits.
- Weak learning units appear in later reviews.
- A new bundled exercise module can be added without changing core domain services.
- The application remains usable on desktop and mobile browsers.

---

## 19. Risks and Mitigations

### Architecture over-engineering

**Mitigation:** static bundled modules, no marketplace, no sandbox, no distributed architecture, one end-to-end workflow first.

### Unstable extension contracts

**Mitigation:** build at least three exercise modules against the same interface, version contracts, allow breaking changes before v1.0.

### Poor AI output

**Mitigation:** user review, structured generation, prompt versioning, validation, source references.

### Unreliable semantic evaluation

**Mitigation:** deterministic checks first, structured categories, uncertain state, regression tests, manual override.

### Provider cost

**Mitigation:** usage tracking, caching, batching, deterministic evaluation, provider abstraction.

### Scope creep

**Mitigation:** explicit exclusions and phase gates.

---

## 20. Acceptance Criteria

The MVP is accepted when:

1. A user can create a lesson from pasted English text.
2. The source text is preserved.
3. Candidate learning units are extracted.
4. The user can accept, edit, reject, and add learning units.
5. At least three exercise modules are available through the Exercise Registry.
6. The user can generate and complete exercises.
7. Closed exercises are checked deterministically where possible.
8. Open answers can be evaluated semantically.
9. Feedback distinguishes correct, acceptable, partial, incorrect, and uncertain results.
10. Attempts are saved.
11. Weak learning units are identified.
12. Due reviews can be retrieved.
13. The application runs through Docker Compose.
14. The main workflow works on desktop and mobile browsers.
15. AI features use provider abstractions.
16. Bundled modules register through public module contracts.
17. A proof-of-concept exercise module can be added without modifying core domain services.
18. AI failures do not cause loss of lesson or attempt data.

---


## 20.1 Architectural Success Criteria

The architecture is considered successful if:

- a new exercise module can be added without modifying the Core;
- a new language module can be be added without changing existing exercise modules;
- AI providers are interchangeable;
- official modules use only documented public APIs;
- frontend and backend modules evolve independently through shared contracts;
- runtime plugins can be introduced later without redesigning the Core.

---

## 21. Development Roadmap

### Phase 0 — Product Discovery
- PRD
- ADR foundation
- research
- UX concept
- domain model
- MVP definition

### Phase 1 — Platform Foundation
- Core Kernel
- Module Host
- Capability Registry
- Command Bus
- Event Bus
- Module Manifest
- infrastructure
- Docker
- React
- FastAPI

### Phase 2 — First Learning Workflow (MVP)
- English language module
- plain-text importer
- chunk extraction
- Gap Fill
- Chunk Completion
- Sentence Reconstruction
- semantic evaluation
- deterministic evaluation
- review queue
- responsive web UI

### Phase 3 — Learning Platform Expansion
- additional exercise modules
- analytics
- richer review
- grammar modules
- interview mode

### Phase 4 — AI Platform
- multiple providers
- AI feature modules
- prompt versioning
- caching
- cost tracking

### Phase 5 — Multi-language Platform
- additional language modules
- language-specific NLP
- localization

### Phase 6 — Client Expansion
- PWA
- desktop (Tauri)
- mobile companion
- voice capture

### Phase 7 — Integrations & MCP
- import/export modules
- MCP
- Obsidian
- Anki
- cloud integrations

### Phase 8 — Community Platform
- external SDK
- runtime loader
- permissions
- signed packages
- marketplace
- sandboxing

---

## 22. Open Questions for GSD Research

### Product and pedagogy

1. Maximum source-text length?
2. Default number of extracted learning units?
3. Must users select target chunks before generation?
4. Fixed or adaptive exercise progression?
5. When is a unit mastered?
6. Should review target units, exercises, source sentences, or a combination?
7. Are manual exercises required in MVP?

### Evaluation

8. Which answer types require AI?
9. How are accepted variants stored?
10. Can a valid paraphrase become a reusable accepted answer?
11. How are grammar and meaning weighted?
12. How is evaluator disagreement handled?
13. What evidence is shown when AI rejects an answer?

### Architecture

14. Minimum useful Module Manifest schema?
15. Which capabilities belong in API v1?
16. Must command bus and event bus be separate in MVP?
17. Simplest SQLite module-data isolation?
18. How are frontend and backend module versions coordinated?
19. Module packaging strategy in the monorepo?
20. Compatibility policy before v1.0?

### AI

21. Default MVP provider?
22. Structured-output validation library?
23. Prompt-versioning strategy?
24. Cache scope?
25. Cost limits?
26. Synchronous requests or background jobs?

### Scheduling

27. Fixed intervals, simplified SM-2, or FSRS?
28. How does self-rating affect scheduling?
29. How do repeated failures change difficulty?

### Data and identity

30. Is authentication required for local MVP?
31. Multiple local profiles?
32. Deletion and retention model?
33. Export format?
34. Required AI metadata?

### UX

35. Minimum screens?
36. Generation progress and failure states?
37. Immediate feedback or end-of-session feedback?
38. How much source text remains visible at each stage?
39. How does the learner switch between exact recall and free paraphrase?

### MCP and integrations

40. Which application commands should eventually be exposed through MCP?
41. MCP client, server, or both first?
42. Permission boundary for external tools?
43. Highest-value early integration?

---

## 23. Recommended GSD Outputs

GSD should derive and maintain:

- project definition;
- product research;
- architecture decision records;
- module contract specifications;
- repository structure;
- domain model;
- API specification;
- database model;
- UX flows;
- roadmap;
- phase plans;
- test strategy;
- backlog;
- deployment documentation.

---

## 24. Appendix A — Initial Module Map

```text
Core
├── Lesson Service
├── Learning Unit Registry
├── Exercise Registry
├── Attempt Service
├── Review Service
├── Module Host
├── Capability Registry
├── Command Bus
└── Event Bus

Bundled Modules
├── language-en
├── import-plain-text
├── learning-unit-lexical-chunk
├── exercise-gap-fill
├── exercise-chunk-completion
├── exercise-sentence-reconstruction
├── exercise-keyword-recall
├── ai-provider-openai-compatible
├── ai-feature-chunk-extractor
├── ai-feature-semantic-evaluator
└── scheduler-simple
```

---

## 25. Appendix B — Educational Foundations

- retrieval practice;
- active recall;
- lexical approach;
- lexical chunks and collocations;
- desirable difficulty;
- spaced repetition;
- progressive scaffolding;
- delayed recall;
- semantic feedback;
- learner-controlled correction.

The application must not enforce exact memorization when a natural, correct, meaning-preserving alternative exists.

---

## 26. Document Governance

This PRD is the baseline product document for GSD initialization.

Changes that affect MVP scope, product principles, primary user, core workflow, extension architecture, module parity, technology constraints, or acceptance criteria should update this document or create an Architecture Decision Record during GSD.

Detailed implementation decisions should not be added to the PRD unless they become product-level constraints.
