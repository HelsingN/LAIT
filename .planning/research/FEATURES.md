# Feature Research

**Domain:** Progressive-retrieval language learning from user-owned professional text
**Researched:** 2026-07-15
**Confidence:** HIGH for learning-loop features; MEDIUM for scheduler and AI-quality thresholds pending product data

## Research Boundary

The PRD defines the product and MVP. This document classifies and strengthens that scope; it does not substitute competitor conventions for the approved vision. Features absent from the PRD are recommendations only and default to deferred unless they are necessary to make an approved requirement reliable or testable.

## Feature Landscape

### Table Stakes for This MVP

| Feature | Why Expected | Complexity | Implementation Notes |
|---------|--------------|------------|----------------------|
| Lesson lifecycle and immutable original source | User-owned material is the starting point and evidence for every generated artifact | MEDIUM | Store source revisions separately; generated content points to a source revision and offsets/snippets. |
| Visible analysis progress and recoverable failure | AI analysis can take seconds or minutes and fail independently | MEDIUM | Durable job status, retry, cancel, safe error explanation, and resume after refresh. |
| Source-grounded candidate units | Learners must trust why a phrase was selected | HIGH | Preserve exact occurrence, sentence context, unit type, rationale, confidence, and analyzer/prompt version. |
| Review-before-generation | AI output is advisory and the learner controls what becomes practice | MEDIUM | Accept, edit, reject, restore, and manually add; retain provenance after edits. |
| Four progressive exercise types | Approved MVP commitment and the mechanism for fading support | HIGH | Gap Fill → Chunk Completion → Sentence Reconstruction → Keyword Recall, all through the registry. |
| One-exercise-at-a-time session | Reduces split attention and makes attempt semantics clear | MEDIUM | Stable progress, keyboard/mobile input, retry/reveal/continue, and refresh recovery. |
| Deterministic grading where possible | Fast, explainable, cheap, and reliable for closed tasks | MEDIUM | Language module owns normalization; accepted variants are explicit and auditable. |
| Semantic grading with uncertainty | Open production requires meaning-aware feedback without pretending certainty | HIGH | Structured categories, evidence from target chunks, short feedback, natural alternative, and `uncertain`. |
| Attempt history linked to learning units | Required for weak-unit detection and later review | MEDIUM | Save every submission, even retry/reveal paths; distinguish assisted from independent success. |
| Due-review queue and self-rating | Retrieval must recur over time, and difficulty is partly learner-observed | MEDIUM | Simple replaceable scheduler using time, recent correctness, failures, hints/reveal, and self-rating. |
| Graceful offline/provider failure | Local learning data remains useful when AI is unavailable | MEDIUM | Existing lessons, units, attempts, and review work without provider access; generation surfaces retryable status. |
| Responsive and accessible primary flow | Mobile-browser usability is an acceptance criterion, not a later polish item | MEDIUM | Touch targets, virtual-keyboard behavior, visible focus, screen-reader labels, reduced motion, and mobile E2E tests. |
| AI disclosure and traceability | User content may be transmitted externally and grades influence learning | MEDIUM | Provider disclosure before first call; request metadata and prompt/schema versions stored without secrets. |

### Differentiators Already Aligned With the Vision

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Progressive removal of cues | Bridges recognition and independent production instead of stopping at flashcard recall | HIGH | Research on diminishing/progressive cues supports scaffolding hard retrieval, but progression thresholds must be measured. |
| Lexical-chunk-first analysis | Targets reusable professional phrases and collocations rather than isolated vocabulary | HIGH | Formulaic-sequence research supports perceived fluency; show context and allow learner correction. |
| Meaning-preserving paraphrase acceptance | Rewards communicative competence rather than brittle exact memorization | HIGH | Use reference-guided rubric plus deterministic target-chunk evidence and an uncertainty escape hatch. |
| Weakness tracking at learning-unit level | Review targets the actual chunk or structure that caused difficulty | HIGH | Exercise instances must declare which units they test and how strongly. |
| User-owned professional material | Practice maps directly to interviews and real explanations | MEDIUM | Add sample text only as onboarding help; never displace user content as the product center. |
| Mod-First official-module parity | Enables new methods without core rewrites and validates future community contracts | HIGH | Conformance tests and a proof module are product acceptance criteria, not internal-only architecture work. |
| Replaceable AI features and providers | Users can change transport/vendor without rewriting pedagogy | HIGH | Feature prompts/rubrics are versioned separately from provider calls. |

### Reliability Features Required to Make Approved Scope Real

These are implementation-strengthening requirements, not product expansion:

| Feature | Failure Prevented | Complexity |
|---------|-------------------|------------|
| Input limits with visible character/token estimate | Surprise cost, latency, and context truncation | LOW |
| Idempotent analysis/generation commands | Duplicate units/exercises after retry or double tap | MEDIUM |
| Generation provenance and source revision checks | Exercises silently detached from edited source | MEDIUM |
| Manual grading override / “this feedback is wrong” | AI judgment becomes unchallengeable ground truth | LOW |
| Prompt/evaluator regression corpus | Provider or prompt changes degrade grading unnoticed | HIGH |
| Backup/export of local data in a documented format | Local SQLite file becomes a single opaque point of loss | MEDIUM |
| Fresh-install and restart smoke tests | “Docker Compose works” only on the developer machine | MEDIUM |

### Anti-Features

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Automatic acceptance of every extracted unit | Faster lesson creation | Poor candidates propagate into every exercise and poison review data | Require learner review with efficient bulk actions and confidence sorting |
| AI grading for every answer | Seems more intelligent and consistent | Adds cost, latency, nondeterminism, and false judgments where rules suffice | Deterministic-first evaluation with semantic fallback |
| Exact-string grading for open production | Easy to implement | Punishes valid paraphrases and contradicts the product principle of meaning over memorization | Reference-guided semantic rubric plus target-chunk evidence |
| Adaptive algorithm before enough data | Sounds personalized | Unverifiable coefficients create arbitrary scheduling and hide product learning | Transparent simple scheduler; log data needed to evaluate later algorithms |
| Gamification-first streaks and points | Engagement shorthand | Can incentivize easy recognition and daily tapping rather than difficult retrieval | Progress based on independent recall, weak-unit improvement, and review completion |
| Chatbot as the primary interface | Familiar AI interaction | Produces unstable workflows and weak attempt/review semantics | Purpose-built lesson, review, exercise, and feedback states; AI stays behind capabilities |
| Dynamic plugin marketplace in MVP | Demonstrates extensibility dramatically | Adds trust, signing, compatibility, installation, UI loading, and support burden before contracts stabilize | Bundled modules plus conformance suite and proof module |
| Authentication “just in case” | Common web-app convention | Adds no learning validation in a local one-user release | No login; keep identity boundary injectable for later |
| Paragraph Recall before the loop is stable | Natural next difficulty step | Expands prompting, grading, UI, and data complexity before four committed exercises are proven | Defer until four modules and review loop meet quality metrics |

## Feature Dependencies

```text
Module contracts + composition root
    ├──> Language normalization capability
    ├──> Importer capability
    ├──> Exercise registry + renderer registry
    ├──> AI capability registry
    └──> Scheduler capability

Lesson + immutable source revision
    └──> Durable analysis job
             └──> Candidate learning units + provenance
                      └──> Learner review/acceptance
                               └──> Exercise generation
                                        └──> Exercise session
                                                 └──> Attempts + evaluation
                                                          └──> Weak-unit evidence
                                                                   └──> Due-review queue

Deterministic evaluator ──precedes──> Semantic evaluator
Fake provider + eval corpus ──guards──> Live provider adapter
Responsive shell ──hosts──> Module-contributed exercise renderers
```

### Dependency Notes

- **Generation requires accepted units:** unreviewed AI candidates must not silently become study material.
- **Review requires complete attempt semantics:** correctness alone is insufficient; retry, reveal, hint level, evaluator confidence, and self-rating change scheduling evidence.
- **Exercise modules require language capabilities:** normalization and tokenization belong to `language-en`, avoiding duplicated English assumptions.
- **Frontend module registration requires stable exercise-instance contracts:** renderer choice, payload schema, accessibility metadata, and answer schema must be versioned together.
- **Semantic evaluation requires a regression harness before it becomes authoritative:** human-curated reference cases calibrate automated grades and the `uncertain` boundary.
- **AI usage tracking requires job/request correlation from the first call:** reconstructing cost and prompt provenance later is unreliable.

## MVP Definition

### Launch With (v1)

- [ ] Create, rename, edit, archive, and delete lessons from pasted English text; preserve original/revision history.
- [ ] Analyze a bounded source through a durable, visible job and show source-grounded candidate units.
- [ ] Accept, edit, reject, restore, and manually add learning units.
- [ ] Generate and complete all four approved exercise modules through public registries.
- [ ] Apply deterministic evaluation first and structured semantic evaluation for open answers.
- [ ] Show concise, evidence-linked feedback with correct/acceptable/partial/incorrect/uncertain categories.
- [ ] Persist every attempt and identify weak learning units.
- [ ] Retrieve and complete a due-review queue using the simple scheduler and learner self-rating.
- [ ] Preserve useful local data and navigation during provider outages.
- [ ] Run the primary flow through Docker Compose on desktop and mobile browser widths.
- [ ] Demonstrate a proof exercise module can be added without changing core domain services.
- [ ] Record AI provenance, usage, cost data when available, and disclosure state.

### Add After Validation (v1.x)

- [ ] Paragraph Recall — only after the four-module funnel is measured and stable.
- [ ] Data export/backup UI — elevate earlier if users store irreplaceable professional material during pilots.
- [ ] Rich progress analytics — add once metrics answer actionable learner questions rather than decorate dashboards.
- [ ] More sophisticated scheduling — require evidence that the simple scheduler is the limiting factor.
- [ ] Manual exercise authoring — add if learner review shows generated coverage gaps that editing units cannot solve.
- [ ] Multiple local profiles — add when shared-device use is observed.

### Future Consideration (v2+)

- Additional languages and language selection.
- PDF/DOCX/web/subtitle/YouTube importers.
- Voice, dictation, shadowing, pronunciation, and interview simulation.
- PWA, Tauri, and mobile companion clients.
- MCP, Anki, Obsidian, NotebookLM, and other integrations.
- Multiple AI providers, local models, and capability routing.
- External SDK, runtime module loading, permissions, signatures, marketplace, and sandboxing.
- Authentication, cloud sync, teams, teachers, classrooms, subscriptions, and multi-tenancy.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Source → reviewed units → exercises end-to-end | HIGH | HIGH | P1 |
| Four progressive exercises | HIGH | HIGH | P1 |
| Deterministic + semantic evaluation | HIGH | HIGH | P1 |
| Attempts, weak units, and due review | HIGH | HIGH | P1 |
| Durable AI jobs and failure recovery | HIGH | MEDIUM | P1 |
| Mobile/desktop responsive workflow | HIGH | MEDIUM | P1 |
| Module contract proof and conformance suite | HIGH | HIGH | P1 |
| AI disclosure/provenance/cost logging | HIGH | MEDIUM | P1 |
| Local backup/export | MEDIUM | MEDIUM | P2 |
| Paragraph Recall | MEDIUM | HIGH | P2 |
| Analytics dashboard | MEDIUM | MEDIUM | P2 |
| Advanced scheduler | MEDIUM | HIGH | P2 |
| Gamification | LOW | MEDIUM | P3 |

## Competitor Pattern Analysis

| Capability | Conventional Flashcards | General AI Assistants | Source-Grounded Study Tools | AI Language Coach Approach |
|------------|-------------------------|-----------------------|-----------------------------|----------------------------|
| User-owned source | Manual card creation | Prompt context, usually ephemeral | Strong source grounding | Persistent lesson source with revision/provenance |
| Retrieval progression | Usually fixed card front/back | Ad hoc prompt sequence | Often comprehension-centered | Explicit diminishing support across module types |
| Paraphrase evaluation | Usually exact/manual | Flexible but unstable | Not a persistent learning grade | Structured semantic rubric plus uncertainty and override |
| Weakness model | Card-level scheduling | Usually absent | Usually absent | Attempts linked to learning units across exercises |
| Extensibility | Add-ons vary by product | Tool/API integrations | Product-specific | Official modules use future public extension contracts |
| Review queue | Strong in flashcard tools | Usually absent | Limited | Simple replaceable scheduling based on actual unit evidence |

The product should borrow reliable scheduling transparency and user control from flashcard systems without becoming card-centric; borrow flexible generation from AI assistants without becoming chat-centric; and borrow source visibility from grounded study tools without stopping at comprehension.

## Learning-Evidence Implications

- Retrieval practice improves long-term learning compared with repeated study; repeated successful retrieval matters, so attempts should not disappear after the first correct answer.
- Distributed practice has broad empirical support; the MVP needs an actual due queue even if the algorithm is simple.
- Diminishing/progressive cues can help when unaided retrieval is initially too difficult, but the easiest level should not become a permanent comfort zone. Track cue level and independent success separately.
- Formulaic sequences can improve perceived oral proficiency and justify chunk-centered practice, but automatic extraction is not ground truth. Context, learner review, and manual correction remain essential.
- AI-evaluated quality must be calibrated against human judgments. Task-specific examples, edge cases, and pass/fail/category rubrics are more useful than a generic “quality score.”

## Sources

- [Karpicke & Roediger, “The Critical Importance of Retrieval for Learning”](https://doi.org/10.1126/science.1152408) — retrieval practice and repeated testing.
- [Cepeda et al., distributed-practice meta-analysis](https://pubmed.ncbi.nlm.nih.gov/16719566/) — spacing evidence across verbal recall tasks.
- [Fiechter & Benjamin, diminishing-cues retrieval practice](https://pubmed.ncbi.nlm.nih.gov/28849580/) — scaffolded retrieval when standard testing is too difficult.
- [Progressive retrieval practice for image-word pairs](https://pubmed.ncbi.nlm.nih.gov/35638593/) — graded cues and delayed performance.
- [Boers et al., formulaic sequences and perceived oral proficiency](https://eric.ed.gov/?id=EJ805192) — lexical-sequence rationale.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — task-specific evals, representative cases, continuous evaluation, and human calibration.
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) — adversarial testing, source visibility, input constraints, and human review.
- Product baseline and competitor framing: `docs/prd/PRD.md`.

---
*Feature research for: AI Language Coach*
*Researched: 2026-07-15*
