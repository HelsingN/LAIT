# AI Language Coach

## What This Is

AI Language Coach is a local-first, responsive web application that helps adult B1–B2 English learners—initially IT professionals preparing for interviews and professional conversations—turn passive language knowledge into active speaking ability. It transforms authentic user-owned text into reviewed lexical learning units, progressively harder retrieval exercises, concise deterministic or semantic feedback, and scheduled review of weak material.

The initial product is deliberately small and single-user, while its modular-monolith architecture establishes public extension contracts so exercise types, languages, AI providers and features, importers, schedulers, integrations, and future clients can evolve without expanding or rewriting the core domain.

## Core Value

A learner can turn their own professional English text into reliable progressive-retrieval practice that helps them recall and produce useful language independently.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] A learner can create and manage a lesson from pasted English text while the original source remains unchanged.
- [ ] AI-assisted analysis extracts source-grounded lexical chunks, collocations, phrasal verbs, and useful sentence patterns for learner review.
- [ ] A learner can accept, edit, reject, and manually add learning units before exercises are generated.
- [ ] The MVP provides Gap Fill, Chunk Completion, Sentence Reconstruction, and Keyword Recall as four bundled exercise modules.
- [ ] Exercises progressively reduce support and allow the learner to continue, retry, or reveal the source.
- [ ] Closed exercises use deterministic or normalized evaluation wherever feasible.
- [ ] Open answers use replaceable semantic evaluation that accepts natural meaning-preserving paraphrases and can report uncertainty.
- [ ] Feedback shows the submitted answer, reference answer, result category, concise explanation, and an optional natural alternative.
- [ ] Every submitted attempt is persisted and associated with the learning units it exercises.
- [ ] Weak learning units are identified and returned through a due-review queue using a simple replaceable scheduler.
- [ ] The learner can rate review material as easy, difficult, or mastered.
- [ ] The full workflow is usable at desktop and mobile browser widths without manual database or configuration changes.
- [ ] The application runs locally through Docker Compose with no login and one local learner context.
- [ ] Bundled modules register through versioned public contracts and do not rely on undocumented privileged access.
- [ ] Exercise, language, AI-provider, AI-feature, importer, and scheduler behavior remains outside the small core and is independently testable.
- [ ] AI provider failures do not corrupt or hide stored lessons, attempts, or review data.
- [ ] AI calls are traceable by provider, model, feature, prompt version, timestamp, usage, and cost where available.

### Out of Scope

- Authentication, multiple profiles, and multi-tenant SaaS — the MVP opens directly into one local learner context.
- Languages other than English and a language picker — only the bundled English language module is exposed in the MVP.
- Paragraph Recall — optional follow-on work only after the committed four exercise modules and full workflow are stable.
- Native mobile and desktop applications — the MVP is a responsive web application; PWA, Tauri, and mobile companions are future clients.
- Runtime installation of third-party modules, a marketplace, sandboxing, signed packages, and permission enforcement — MVP modules are trusted, bundled, and registered at build time.
- PDF, DOCX, web page, YouTube, subtitle, and note imports — MVP input is pasted plain text.
- Speech recognition, pronunciation scoring, speech synthesis, and local AI execution — deferred beyond the text-first MVP.
- Teacher, classroom, team, social, sharing, payment, and enterprise administration features — they do not serve the first single-learner validation.
- Production MCP, Anki, NotebookLM, Obsidian, and cloud integrations — application commands should remain adapter-ready, but integrations are not MVP deliverables.
- Microservices and distributed messaging — a modular monolith with an in-process event bus is sufficient for the first release.
- Advanced adaptive scheduling such as FSRS — the MVP uses a simple replaceable scheduler.

## Context

Intermediate learners often recognize substantially more vocabulary and grammar than they can retrieve under speaking pressure. Existing tools split the problem: flashcard systems provide repetition but require prepared cards, source-grounded tools support comprehension rather than structured recall, and general AI assistants lack a persistent learning model, stable workflows, and a due-review queue.

The primary learner understands technical material but struggles to produce fluent self-introductions, interview stories, and explanations of professional experience. They prefer authentic personal material, lexical chunks over isolated words, short actionable feedback over grammar lectures, and acceptance of natural paraphrases rather than exact memorization.

The learning sequence progresses from recognition through chunk completion, sentence reconstruction, keyword recall, and eventually free production. Meaning, user control, desirable difficulty, and recycling of weak material take priority over gamification or rigid reproduction of the source.

The baseline PRD is `docs/prd/PRD.md`. It governs product intent, MVP scope, architectural constraints, module parity, technology constraints, and acceptance criteria. Detailed APIs, schemas, package boundaries, background-job strategy, UX flows, and scheduling algorithms remain planning and research decisions.

The intended logical architecture is a responsive client over public application and extension contracts, backed by a small core kernel and infrastructure adapters. Official modules must use the same documented contracts intended for future community modules. Provider modules define how an AI model is called; AI-feature modules define why it is called. MCP and other integrations consume application commands rather than private storage.

## Constraints

- **Frontend**: React and TypeScript responsive web UI — required by the PRD and future module-renderer strategy.
- **Backend**: Python and FastAPI modular monolith — required by the PRD; core logic must remain framework-independent where practical.
- **Database**: SQLite for MVP with a credible migration path to PostgreSQL — supports local deployment without locking future growth to opaque storage.
- **Deployment**: Docker and Docker Compose — the complete local workflow must start without manual database edits.
- **Architecture**: Small core, hexagonal boundaries, dependency inversion, capability registry, commands, and domain/application events — modules depend on public capabilities, not concrete implementations.
- **Extensibility**: Design extension contracts for future runtime loading, but implement only trusted build-time bundled modules in MVP — avoids premature marketplace and sandbox complexity.
- **Module parity**: Official modules receive no undocumented privileged access — validates that future third-party modules can use the same contracts.
- **Language**: English-only processing and no language picker in MVP — multilingual-safe Unicode storage and directionality-aware contracts must still avoid an English-only redesign later.
- **Identity**: One local learner context with no login — authentication and profile switching are intentionally deferred.
- **Exercises**: All four named exercise modules are MVP commitments — Paragraph Recall is not allowed to jeopardize delivery.
- **Evaluation**: Deterministic checks precede semantic AI evaluation; low-confidence semantic results return `uncertain` — learner trust is more important than forced grading.
- **Reliability**: Source content is immutable unless explicitly edited, secrets never reach source control or the frontend, and AI failure cannot corrupt stored learning data.
- **Performance**: Normal lesson analysis and exercise generation must not freeze the UI; a normal lesson should yield a usable exercise set in under five minutes.
- **Quality**: At least 80% of generated exercises should be usable after learning-unit review, and the core plus modules must be independently testable.
- **Portability**: User content remains user-owned, provider transmission is disclosed, and local-first deployment remains viable.
- **Manual UI verification**: A plan that changes learner-visible UI, navigation, interaction state, or persistence/reopen behavior ends on a blocking Docker human check before the next dependent wave. Vitest and pytest do not replace it. Backend-only plans do not get that checkpoint. Policy: `docs/governance/MANUAL_UI_VERIFICATION.md`.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Optimize the MVP for adult B1–B2 IT professionals learning English | A narrow initial persona makes source material, feedback, and success criteria concrete | — Pending |
| Use progressive retrieval based on lexical chunks and meaning-preserving production | The product exists to convert passive knowledge into active recall, not reward recognition or exact memorization | — Pending |
| Ship as a local single-user web application with no login | Identity work does not validate the learning loop and can be added after product value is proven | — Pending |
| Fix the MVP language to English with no picker | Only one language module is bundled; a single-option selector would add UI without user value | — Pending |
| Require all four exercises: Gap Fill, Chunk Completion, Sentence Reconstruction, and Keyword Recall | The set demonstrates progressive support removal and exercises the common extension contract across varied interaction types | — Pending |
| Separate AI providers from AI features | Provider replacement must not entangle domain intent with vendor transport | — Pending |
| Use a small-core modular monolith with static bundled modules | It validates extension boundaries while preserving MVP delivery speed and operational simplicity | — Pending |
| Design for runtime extensibility but implement build-time extensibility first | Marketplace, sandbox, signing, and dynamic loading are premature before stable contracts exist | — Pending |
| Use public capabilities, commands, events, and versioned manifests for module integration | Official-module parity is an architectural acceptance criterion and prevents private cross-module coupling | — Pending |
| Prefer deterministic evaluation and use semantic AI only where needed | Reliability, cost control, traceability, and graceful degradation improve when AI is not the default grader | — Pending |
| Start with a simple replaceable scheduler | Review behavior must exist in MVP, but advanced adaptive algorithms should not block the end-to-end learning loop | — Pending |
| Stop learner-visible plans for a Docker human check | Automated tests missed a reopen bug that only showed up on the Compose app | `docs/governance/MANUAL_UI_VERIFICATION.md` |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-07-15 after initialization*
