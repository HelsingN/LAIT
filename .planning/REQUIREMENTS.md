# Requirements: AI Language Coach

**Defined:** 2026-07-16
**Core Value:** A learner can turn their own professional English text into reliable progressive-retrieval practice that helps them recall and produce useful language independently.
**Authority:** `docs/prd/PRD.md` and approved initialization decisions; research strengthens implementation but does not redefine scope.

## v1 Requirements

### Lessons and Sources

- [x] **LESS-01**: Learner can create a lesson by pasting English plain text without configuring an account or language.
- [x] **LESS-02**: Learner can view a list of active lessons and open any lesson in the local learner context.
- [ ] **LESS-03**: Learner can rename an existing lesson.
- [ ] **LESS-04**: Learner can edit lesson source text while the previously analyzed source remains preserved as an immutable revision.
- [ ] **LESS-05**: Learner can archive a lesson and restore it without losing its source, learning units, exercises, attempts, or review history.
- [ ] **LESS-06**: Learner can delete a lesson through an explicit confirmation flow whose related-data deletion behavior is stated and applied consistently.
- [ ] **LESS-07**: Learner can always inspect the original source revision used to produce a learning unit, exercise, or evaluation reference.

### Learning-Unit Analysis

- [ ] **ANLY-01**: Learner can request analysis of a lesson and immediately receive visible queued, running, completed, or failed status rather than waiting on one HTTP request.
- [ ] **ANLY-02**: Learner can refresh or reopen the application during analysis and observe the same job continue or reach a recoverable failure without duplicate learning units.
- [ ] **ANLY-03**: Learner can receive candidate lexical chunks, collocations, phrasal verbs, and useful sentence patterns extracted from the selected source revision.
- [ ] **ANLY-04**: Learner can see each candidate unit in its original sentence or source occurrence before deciding whether to study it.
- [ ] **ANLY-05**: Learner can accept an extracted learning unit.
- [ ] **ANLY-06**: Learner can edit an extracted learning unit while retaining its source occurrence and generation provenance.
- [ ] **ANLY-07**: Learner can reject an extracted learning unit and undo that rejection before leaving the review workflow.
- [x] **ANLY-08**: Learner can manually add a learning unit linked to the lesson and, when applicable, a source occurrence.
- [ ] **ANLY-09**: Learner can explicitly re-analyze an edited source revision without silently replacing accepted units or historical exercises from an earlier revision.

### Exercises and Sessions

- [x] **EXER-01**: Learner can generate exercises only from accepted learning units and can see a recoverable status while generation runs.
- [x] **EXER-02**: Learner can start an exercise session for a lesson and receive one exercise at a time.
- [x] **EXER-03**: Learner can complete Gap Fill exercises supplied through the Exercise Registry.
- [ ] **EXER-04**: Learner can complete Chunk Completion exercises supplied through the Exercise Registry.
- [ ] **EXER-05**: Learner can complete Sentence Reconstruction exercises supplied through the Exercise Registry.
- [ ] **EXER-06**: Learner can complete Keyword Recall exercises supplied through the Exercise Registry.
- [x] **EXER-07**: Learner can submit an answer, view feedback, and continue to the next exercise without leaving the session.
- [ ] **EXER-08**: Learner can retry an exercise after feedback, with each submission retained as a distinct attempt.
- [ ] **EXER-09**: Learner can reveal the relevant source or reference, with that assistance recorded rather than counted as independent recall.
- [ ] **EXER-10**: Learner can resume an interrupted session without losing already submitted attempts or its current progress.
- [ ] **EXER-11**: Learner receives progressively reduced support across the four exercise types while the product records the cue or assistance level used.

### Evaluation and Feedback

- [x] **EVAL-01**: Learner receives deterministic evaluation for selected options, exact missing content, token ordering, and other closed answers whenever a reliable rule exists.
- [ ] **EVAL-02**: Learner receives normalized deterministic comparison that applies English-module rules for whitespace, capitalization, punctuation, contractions, and configured accepted variants.
- [ ] **EVAL-03**: Learner can submit an open answer for semantic evaluation without requiring exact reproduction of the source wording.
- [x] **EVAL-04**: Learner receives one explicit result category: correct, acceptable, partial, incorrect, or uncertain.
- [x] **EVAL-05**: Learner can see the submitted answer, reference answer or meaning, concise explanation, target chunks used or missed, and an optional natural alternative.
- [ ] **EVAL-06**: Learner can inspect the relevant original source while reviewing feedback.
- [ ] **EVAL-07**: Learner's submitted attempt is saved before an external semantic-evaluation request, so provider failure cannot lose the answer.
- [ ] **EVAL-08**: Learner receives `uncertain` or an unable-to-evaluate state when the semantic evaluator cannot support a reliable judgment.
- [ ] **EVAL-09**: Learner can flag or override an AI evaluation that they believe is wrong without deleting the original evaluation record.
- [ ] **EVAL-10**: Maintainer can compare any prompt, rubric, model, or provider change against a versioned human-curated corpus containing valid paraphrases, meaning drift, grammar-only errors, missing target chunks, and uncertainty cases before activation.

### Attempts and Review

- [ ] **REVW-01**: Learner can review a chronological history of every submitted attempt, including retries and revealed or assisted attempts.
- [ ] **REVW-02**: Learner can see which learning units were targeted and which were weak for an evaluated attempt.
- [ ] **REVW-03**: Learner can retrieve a queue of learning units due for review.
- [ ] **REVW-04**: Learner receives review scheduling based on recent correctness, failure count, time since review, assistance or reveal use, and learner difficulty rating through a replaceable scheduler module.
- [ ] **REVW-05**: Learner can rate a reviewed item as easy, difficult, or mastered and see that choice affect its review state.
- [ ] **REVW-06**: Learner can see a concise explanation of why a review item is due.
- [ ] **REVW-07**: Learner can complete due-review exercises and have their outcomes feed future weak-unit and scheduling decisions.
- [ ] **REVW-08**: Maintainer can recompute or migrate review state because the scheduler module ID, algorithm version, parameters, inputs, and outcome are recorded.

### Mod-First Extension Contracts

- [x] **MODL-01**: Maintainer can start the application only when every bundled module manifest is valid, API-compatible, uniquely identified, and has resolvable declared dependencies.
- [x] **MODL-02**: Maintainer can inspect which bundled modules and capabilities are active without accessing private module implementation details.
- [ ] **MODL-03**: Maintainer can add a bundled exercise module through the public exercise contracts, static module catalog, and frontend renderer registry without modifying core domain services.
- [ ] **MODL-04**: Maintainer can run the same exercise-module conformance suite against Gap Fill, Chunk Completion, Sentence Reconstruction, Keyword Recall, and a proof-of-concept exercise module.
- [ ] **MODL-05**: Maintainer can register language behavior through a language-module contract that provides normalization, tokenization, punctuation handling, and directionality metadata without embedding English rules in core services.
- [ ] **MODL-06**: Maintainer can replace an AI provider behind declared capabilities without changing AI feature prompts, rubrics, or core domain logic.
- [ ] **MODL-07**: Maintainer can replace an AI feature implementation without exposing provider transport or credentials to core services.
- [ ] **MODL-08**: Maintainer can register a plain-text importer and simple scheduler through their category-specific public contracts.
- [ ] **MODL-09**: Maintainer can evolve public extension contracts through explicit API and schema versions with compatibility validation and migration notes.
- [ ] **MODL-10**: Maintainer can verify that bundled modules use only documented public contracts and never import another module's private implementation or modify its private storage.
- [ ] **MODL-11**: Maintainer can store core-owned records separately from typed or schema-versioned module-owned data while keeping each component responsible for its migrations.
- [ ] **MODL-12**: Integration developer can invoke documented application commands and queries without reading or writing internal database tables, preserving a future MCP adapter boundary.

### AI Operations, Privacy, and Reliability

- [ ] **AIOP-01**: Maintainer can configure an OpenAI-compatible provider entirely inside its provider adapter, with no vendor SDK or endpoint dependency in core or AI-feature modules.
- [ ] **AIOP-02**: Maintainer receives schema validation and domain validation of AI outputs before generated learning units, exercises, or evaluations enter core-owned records.
- [ ] **AIOP-03**: Maintainer can trace every AI request by provider, endpoint class, model, feature, prompt version, output-schema version, timestamp, latency, job/correlation ID, and disposition.
- [ ] **AIOP-04**: Maintainer can inspect AI token or usage data and estimated cost by feature and request when the provider supplies the necessary metrics.
- [ ] **AIOP-05**: Learner can retry a retryable AI failure without duplicating accepted learning units, exercises, or attempts.
- [ ] **AIOP-06**: Learner retains access to stored lessons, learning units, attempts, feedback, and due-review data while the AI provider is unavailable.
- [ ] **AIOP-07**: Learner is told which configured provider may receive source text or answers before the first external transmission.
- [ ] **AIOP-08**: Learner's provider secrets are never delivered to the browser, written to source control, or included in normal application logs.
- [ ] **AIOP-09**: Learner's pasted text is treated as untrusted data, separated from model instructions, input-limited, and unable to grant the model application tools or privileges.
- [ ] **AIOP-10**: Learner sees model-generated feedback as sanitized text or safely rendered restricted markup that cannot execute active content.
- [ ] **AIOP-11**: Maintainer can test AI features with a deterministic fake provider without network access or paid API calls.
- [ ] **AIOP-12**: Maintainer can distinguish retryable provider failures, permanent validation failures, refusals, and uncertain semantic results without corrupting lesson or attempt data.

### Platform, Portability, and Quality

- [ ] **PLAT-01**: Learner can complete the entire lesson-to-review workflow at supported desktop browser widths.
- [ ] **PLAT-02**: Learner can complete the entire lesson-to-review workflow at supported mobile browser widths using touch and the on-screen keyboard.
- [ ] **PLAT-03**: Learner can run the application locally through a documented Docker Compose command that performs required migrations and reaches a health-checked ready state.
- [ ] **PLAT-04**: Learner's SQLite data survives normal container restart and can follow a documented migration path to PostgreSQL without changing core domain contracts.
- [ ] **PLAT-05**: Learner's multilingual Unicode source, answers, and metadata are preserved as UTF-8 without destructive normalization even though the MVP processes English only.
- [ ] **PLAT-06**: Learner can continue interacting with the UI while normal analysis or exercise generation runs, with no frozen page or unexplained indefinite spinner.
- [ ] **PLAT-07**: Learner can receive a complete exercise set within five minutes for a documented normal-size lesson under the reference provider and environment.
- [ ] **PLAT-08**: Product validation can demonstrate that at least 80% of generated exercises are usable after learning-unit review on the agreed evaluation sample.
- [x] **PLAT-09**: Maintainer can generate a type-safe TypeScript API client from the FastAPI OpenAPI 3.1 contract and detect an unreviewed contract/client mismatch in CI.
- [ ] **PLAT-10**: Maintainer can test core services, persistence adapters, and each module independently.
- [ ] **PLAT-11**: Maintainer can verify the primary workflow on Chromium plus targeted WebKit and mobile-emulation projects.
- [ ] **PLAT-12**: Maintainer can verify a fresh-volume startup, application restart, interrupted AI job, concurrent session/job writes, database migration, and data persistence without manual database edits.
- [ ] **PLAT-13**: Maintainer can operate SQLite in WAL mode on local storage with bounded write transactions, busy handling, and a documented checkpoint and consistent backup/restore procedure.

## v2 Requirements

Deferred beyond the initial release and not mapped to the v1 roadmap.

### Learning Expansion

- **LRN2-01**: Learner can complete Paragraph Recall after the four v1 exercise modules are validated.
- **LRN2-02**: Learner can author exercises manually when generation and learning-unit editing are insufficient.
- **LRN2-03**: Learner can use richer analytics that explain progress and persistent weaknesses.
- **LRN2-04**: Learner can use an advanced evidence-validated scheduler such as FSRS or another adaptive algorithm.

### Language and Media

- **LANG-01**: Learner can select and study additional target languages through language modules.
- **LANG-02**: Learner can use localized and right-to-left interfaces where applicable.
- **MEDI-01**: Learner can practice dictation, shadowing, pronunciation, interview simulation, or other voice-enabled exercises.

### Imports, Exports, and Integrations

- **IMPT-01**: Learner can import Markdown, PDF, DOCX, subtitles, YouTube transcripts, web pages, or notes through importer modules.
- **EXPT-01**: Learner can export lessons and learning data to documented Markdown, JSON, CSV, Anki, or Obsidian formats.
- **INTG-01**: Integration developer can expose selected application commands through a production MCP adapter.
- **INTG-02**: Learner can connect approved Anki, Obsidian, NotebookLM, or cloud integrations.

### Platform Evolution

- **CLNT-01**: Learner can install a PWA, Tauri desktop client, or mobile companion.
- **IDEN-01**: Multiple learners can use separate local profiles or authenticated synchronized accounts.
- **AIPR-01**: Learner can select among multiple cloud or local AI providers through capability routing.
- **PLUG-01**: Maintainer can install external runtime modules with enforced permissions, signatures, compatibility checks, trust levels, and sandboxing.
- **PLUG-02**: Learner can discover approved external modules through a marketplace.

## Out of Scope for v1

| Feature | Reason |
|---------|--------|
| Authentication, multiple profiles, and multi-tenant SaaS | The approved MVP opens directly into one local learner context; identity work does not validate learning value. |
| Languages other than English or a language picker | Only `language-en` is bundled; contracts remain future-safe without exposing a single-option selector. |
| Paragraph Recall | Must not jeopardize the four committed exercise modules and complete review loop. |
| Native mobile or desktop application | Responsive web is the primary platform; other clients are v2+. |
| Runtime third-party code, marketplace, sandboxing, signing, and enforced third-party permissions | Contracts must stabilize through bundled official modules first. |
| PDF, DOCX, web, YouTube, subtitle, and note import | Plain pasted text is sufficient to validate the MVP loop. |
| Speech recognition, pronunciation scoring, speech synthesis, and local AI | Text-first production and evaluation are the MVP learning surface. |
| Teacher, classroom, team, social, sharing, payments, and enterprise administration | They do not serve the first single-learner validation. |
| Production MCP, Anki, NotebookLM, Obsidian, and cloud integrations | Commands remain adapter-ready, but integrations are not MVP deliverables. |
| Microservices and distributed messaging | A modular monolith and in-process events meet current scale and deployment goals. |
| Advanced adaptive scheduling | A simple transparent replaceable scheduler must be validated first. |
| Complex gamification | Retrieval quality and independent production take priority over streaks, points, or social engagement. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| LESS-01 | Phase 1 | Complete |
| LESS-02 | Phase 1 | Complete |
| LESS-03 | Phase 7 | Pending |
| LESS-04 | Phase 7 | Pending |
| LESS-05 | Phase 7 | Pending |
| LESS-06 | Phase 7 | Pending |
| LESS-07 | Phase 2 | Pending |
| ANLY-01 | Phase 2 | Pending |
| ANLY-02 | Phase 2 | Pending |
| ANLY-03 | Phase 2 | Pending |
| ANLY-04 | Phase 2 | Pending |
| ANLY-05 | Phase 2 | Pending |
| ANLY-06 | Phase 2 | Pending |
| ANLY-07 | Phase 2 | Pending |
| ANLY-08 | Phase 1 | Complete |
| ANLY-09 | Phase 7 | Pending |
| EXER-01 | Phase 1 | Complete |
| EXER-02 | Phase 1 | Complete |
| EXER-03 | Phase 1 | Complete |
| EXER-04 | Phase 3 | Pending |
| EXER-05 | Phase 4 | Pending |
| EXER-06 | Phase 5 | Pending |
| EXER-07 | Phase 1 | Complete |
| EXER-08 | Phase 3 | Pending |
| EXER-09 | Phase 3 | Pending |
| EXER-10 | Phase 4 | Pending |
| EXER-11 | Phase 5 | Pending |
| EVAL-01 | Phase 1 | Complete |
| EVAL-02 | Phase 3 | Pending |
| EVAL-03 | Phase 5 | Pending |
| EVAL-04 | Phase 1 | Complete |
| EVAL-05 | Phase 1 | Complete |
| EVAL-06 | Phase 3 | Pending |
| EVAL-07 | Phase 5 | Pending |
| EVAL-08 | Phase 5 | Pending |
| EVAL-09 | Phase 5 | Pending |
| EVAL-10 | Phase 5 | Pending |
| REVW-01 | Phase 6 | Pending |
| REVW-02 | Phase 6 | Pending |
| REVW-03 | Phase 6 | Pending |
| REVW-04 | Phase 6 | Pending |
| REVW-05 | Phase 6 | Pending |
| REVW-06 | Phase 6 | Pending |
| REVW-07 | Phase 6 | Pending |
| REVW-08 | Phase 6 | Pending |
| MODL-01 | Phase 1 | Complete |
| MODL-02 | Phase 1 | Complete |
| MODL-03 | Phase 1 | Pending |
| MODL-04 | Phase 8 | Pending |
| MODL-05 | Phase 3 | Pending |
| MODL-06 | Phase 2 | Pending |
| MODL-07 | Phase 2 | Pending |
| MODL-08 | Phase 6 | Pending |
| MODL-09 | Phase 8 | Pending |
| MODL-10 | Phase 8 | Pending |
| MODL-11 | Phase 8 | Pending |
| MODL-12 | Phase 1 | Pending |
| AIOP-01 | Phase 2 | Pending |
| AIOP-02 | Phase 2 | Pending |
| AIOP-03 | Phase 2 | Pending |
| AIOP-04 | Phase 5 | Pending |
| AIOP-05 | Phase 7 | Pending |
| AIOP-06 | Phase 7 | Pending |
| AIOP-07 | Phase 2 | Pending |
| AIOP-08 | Phase 5 | Pending |
| AIOP-09 | Phase 2 | Pending |
| AIOP-10 | Phase 5 | Pending |
| AIOP-11 | Phase 5 | Pending |
| AIOP-12 | Phase 2 | Pending |
| PLAT-01 | Phase 9 | Pending |
| PLAT-02 | Phase 9 | Pending |
| PLAT-03 | Phase 1 | Pending |
| PLAT-04 | Phase 9 | Pending |
| PLAT-05 | Phase 3 | Pending |
| PLAT-06 | Phase 2 | Pending |
| PLAT-07 | Phase 9 | Pending |
| PLAT-08 | Phase 5 | Pending |
| PLAT-09 | Phase 1 | Complete |
| PLAT-10 | Phase 1 | Pending |
| PLAT-11 | Phase 9 | Pending |
| PLAT-12 | Phase 9 | Pending |
| PLAT-13 | Phase 9 | Pending |

**Coverage:**
- v1 requirements: 82 total
- Mapped to phases: 82
- Unmapped: 0

---
*Requirements defined: 2026-07-16*
*Last updated: 2026-07-16 after roadmap draft*
