# Pitfalls Research

**Domain:** AI-generated progressive language practice on a local modular platform
**Researched:** 2026-07-15
**Confidence:** HIGH for architectural, AI, and data-integrity risks; MEDIUM for product thresholds pending learner trials

## Critical Pitfalls

### 1. The Mod-First Architecture Exists Only on Paper

**What goes wrong:** Core code switches on exercise IDs, imports official module implementations, understands provider models, or queries module-private tables. A fifth exercise requires core edits despite a registry being present.

**Why it happens:** Direct imports are faster during the first vertical slice, and an untyped service locator can disguise coupling without removing it.

**How to avoid:** Define category-specific public contracts; resolve capabilities at the composition/application boundary; create conformance tests; require at least one proof module to be added without core-domain changes.

**Warning signs:** `if exercise_type == ...` in core, imports from `modules_*` under core, module IDs in domain enums, shared write access to private tables, or tests that instantiate only the full app.

**Phase to address:** Platform contracts before the first exercise; verify again when the third and fourth exercises are added.

---

### 2. Generated Content Loses Its Source and Version

**What goes wrong:** The user edits lesson text and old units/exercises silently appear current; feedback cannot show why a unit exists; regeneration duplicates or overwrites accepted work.

**Why it happens:** Storing one mutable `lesson.text` field is simpler than revision/provenance modeling.

**How to avoid:** Immutable source revisions, explicit analysis/generation runs, occurrence offsets plus excerpt checks, prompt/schema/provider versions, and explicit re-analysis semantics.

**Warning signs:** Generated tables reference only `lesson_id`; edits cascade into historical attempts; no way to reconstruct the input for an AI request; repeated retry increases unit counts.

**Phase to address:** Lesson/source foundation and analysis slice.

---

### 3. AI Work Is Coupled to the HTTP Request

**What goes wrong:** Refreshing or restarting loses work; requests time out; double-clicks create duplicates; the UI spins without meaningful state; provider retries block API capacity.

**Why it happens:** Awaiting a model call or using `BackgroundTasks` produces a quick demo.

**How to avoid:** Durable job state, idempotency keys, leases, bounded retries with jitter, cancel semantics, safe terminal errors, and client polling. Persist learner/domain input before invoking AI.

**Warning signs:** Provider calls inside router functions, only `loading: boolean` in the UI, no job ID, no failed state, or no restart test mid-analysis.

**Phase to address:** First AI analysis phase.

---

### 4. Schema-Conformant AI Output Is Treated as Correct

**What goes wrong:** Valid JSON contains hallucinated source spans, poor chunks, invalid accepted variants, or confidently wrong semantic grades.

**Why it happens:** Structured output eliminates parsing failures and is mistaken for semantic validation.

**How to avoid:** Domain validation after schema validation; verify source quotes/offsets; deterministic checks first; curated human-labeled eval corpus; uncertainty category; learner correction/override; regression gates for prompt/model changes.

**Warning signs:** Tests assert only parse success, no adversarial/edge cases, every open answer receives a decisive label, or model changes ship without comparison.

**Phase to address:** AI feature foundation and every AI-feature phase thereafter.

---

### 5. Feedback Rewards Exact Memorization or Accepts Meaning Drift

**What goes wrong:** Valid paraphrases are rejected, or fluent but semantically wrong answers are accepted. Learners stop trusting feedback.

**Why it happens:** Exact match is reliable but too strict; unconstrained LLM judging is flexible but inconsistent.

**How to avoid:** Exercise-specific rubrics; separate meaning preservation, grammar, and target-chunk evidence; deterministic normalization and known variants first; reference-guided semantic evaluation; concise evidence; `uncertain`; manual override.

**Warning signs:** One evaluator prompt handles every exercise, no distinction between target form and meaning, feedback cannot cite missing/weak content, or evaluator disagreement is unmeasured.

**Phase to address:** Evaluation foundation before open-answer exercises become required.

---

### 6. Scheduler Data Is Too Weak to Support Review

**What goes wrong:** Review dates are based only on a final correct/incorrect flag, so reveal-then-correct and independent recall look identical; weak-unit attribution is arbitrary.

**Why it happens:** The review queue is implemented after exercises and inherits an underspecified attempt model.

**How to avoid:** Capture every attempt, assistance/cue level, retries, reveal, latency (used cautiously), evaluator confidence, unit coverage, and learner rating. Make scheduler decisions explainable and versioned.

**Warning signs:** Attempts are overwritten, an exercise has no declared target units, scheduler state cannot be recomputed, or “mastered” has no explicit effect.

**Phase to address:** Attempt model during the first exercise; scheduler module after evidence semantics stabilize.

---

### 7. SQLite Is Used Without Its Operational Constraints

**What goes wrong:** `database is locked` errors, long write stalls, unbounded WAL growth, corrupted assumptions about network-mounted storage, or backups omit the WAL state.

**Why it happens:** SQLite is treated as “no operations required.”

**How to avoid:** WAL on a local filesystem, short transactions, one controlled writer path for jobs where practical, `busy_timeout`, connection discipline, checkpoint monitoring, consistent backup procedure, migration tests, and a documented PostgreSQL threshold.

**Warning signs:** Provider calls inside DB transactions, long-lived read cursors, multiple worker processes writing freely, DB file placed on network storage, or copied while writes continue without backup API/checkpoint strategy.

**Phase to address:** Persistence foundation; load/restart verification during hardening.

---

### 8. User Text Is Treated as Trusted Instructions

**What goes wrong:** A pasted document changes model behavior, requests secrets, alters output schemas, or injects unsafe rendered Markdown/HTML.

**Why it happens:** Natural-language instructions and content are concatenated into one prompt, and “local single user” is mistaken for trusted content.

**How to avoid:** Delimit and label source as data; provider has no application tools; least-privilege credentials; validate output; sanitize rendered content; cap input/output; adversarial prompt-injection cases; never place secrets in prompts/logs.

**Warning signs:** Raw string concatenation, source content included in system/developer instructions, model output rendered as unsanitized HTML, provider can invoke commands, or logs contain API keys/full sensitive text unnecessarily.

**Phase to address:** AI provider/feature foundation and frontend feedback rendering.

---

### 9. Language Rules Leak Into Core and Exercise Modules

**What goes wrong:** Lowercasing, punctuation, token boundaries, contractions, or word order are hard-coded throughout evaluators; adding Hebrew or another language requires core rewrites.

**Why it happens:** English-only MVP examples make generic string utilities look harmless.

**How to avoid:** `language-en` capabilities for normalization, tokenization, stop words, punctuation, directionality, and accepted-variant rules; Unicode-preserving storage; contract tests with non-ASCII fixtures even before another language ships.

**Warning signs:** `.lower().strip()` in core grading, Latin-letter regexes outside `language-en`, left-to-right CSS assumptions in shared primitives, or exercise payloads that store positions only as naive character counts.

**Phase to address:** Language capability foundation before exercise evaluators.

---

### 10. Responsive Means “Shrunk Desktop”

**What goes wrong:** Virtual keyboards cover answer controls, drag/reorder tasks fail on touch, feedback causes layout jumps, source context is unreadable, or focus is lost after submission.

**Why it happens:** The UI is verified only by resizing a desktop browser late in development.

**How to avoid:** Mobile-first interaction contracts for each exercise renderer, keyboard/touch equivalents, stable focus management, accessible status announcements, safe-area/virtual-keyboard testing, and Playwright mobile Chromium/WebKit projects from the first slice.

**Warning signs:** Hover-only actions, tiny fragment controls, fixed-height viewport assumptions, no mobile E2E project, or renderer contributions without accessibility tests.

**Phase to address:** Application shell and every exercise module; end-to-end verification in hardening.

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| One package with enforced internal boundaries | Faster initial tooling | Boundaries rely on lint/tests rather than distribution metadata | Acceptable through MVP if import rules and contracts are tested |
| Polling job status | Simple and robust | Extra requests and less immediate progress | Acceptable for local MVP; preserve status resource for later SSE |
| Static bundled catalog | Deterministic startup | Rebuild required for modules | Required MVP choice |
| In-process event bus | Minimal infrastructure | No cross-process delivery | Required MVP choice; publish post-commit and keep publisher port |
| SQLite-backed worker queue | No extra service | Single-host throughput and writer contention | Acceptable for local/small hosted use with explicit migration threshold |
| JSON payload for small module settings | Flexible | Weak query/integrity if overused | Acceptable only for small, versioned, schema-validated settings |
| One semantic evaluator model | Faster launch | Provider/model bias and availability risk | Acceptable if behind capability, calibrated, traceable, and uncertain |
| Manual API client during a spike | Fast prototyping | Contract drift | Spike only; replace before feature implementation |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| OpenAI-compatible provider | Assuming every compatible endpoint supports identical structured-output schema, usage fields, errors, and model names | Capability negotiation and provider-specific translation inside the adapter |
| Generated OpenAPI client | Unstable auto-generated operation IDs produce noisy breaking SDKs | Define stable unique operation IDs and diff the generated client in CI |
| Docker Compose | `depends_on` treated as readiness | Add health checks and an explicit successful migration/init dependency |
| SQLite volume | Bind/network filesystem chosen casually | Local named/bind volume with documented backup, ownership, and WAL handling |
| Module manifests | Validation occurs after code activation | Validate all manifests/dependencies into a temporary registry before activation |
| AI usage/cost | Provider response stored without correlation to feature/prompt | Common trace envelope with provider/model/feature/prompt/schema/job IDs |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Provider call inside DB transaction | Lock stalls and slow attempts | Commit intent first; call provider; open short result transaction | Immediately under slow/failing AI calls |
| Unbounded source input | High cost, truncation, long jobs | Visible source limit, token estimate, chunking policy researched per feature | Single unusually large lesson |
| Generating all exercise types in one opaque call | Long latency and all-or-nothing failure | Per-module generation steps, cached validated intermediate units, partial retry | First provider timeout or bad module payload |
| Re-evaluating deterministic answers with AI | Latency/cost spike | Deterministic-first dispatch | Every session at modest use |
| N+1 loading of attempts/units | Slow lesson/review screens | Purpose-built read models and eager/batched queries | Hundreds of attempts |
| SQLite checkpoint starvation | Growing WAL and slow queries | Close reads promptly, monitor WAL, controlled checkpoint/backup | Long overlapping readers/writers |
| Re-rendering full source on every keystroke | Mobile input lag | Isolate answer state and memoize source display | Long lesson text on low-end phones |

## Security and Privacy Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Pasted text can override AI instructions | Prompt injection and corrupted outputs | Treat content as untrusted data, delimit, validate, red-team |
| Provider key exposed to React | Credential theft and uncontrolled spend | Server-only secret injection; provider calls only from backend adapter |
| Full sensitive source/answers logged by default | Privacy leakage | Structured redacted logs; explicit debug opt-in with retention policy |
| Raw model Markdown/HTML rendered | XSS/data exfiltration links | Plain text by default; sanitize allowed Markdown and block active content |
| Provider transmission is implicit | User cannot make informed privacy choice | Clear disclosure and provider endpoint before first transmission |
| Deletion removes lesson but leaves AI traces/jobs | Incomplete data deletion | Define cascade/tombstone rules and verify deletion across owned records |
| Module permissions are decorative but presented as enforced | False security claims | Label MVP vocabulary as declarative metadata; enforce core access boundaries now and document limits |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No editable AI-candidate review | Learner studies poor chunks | Fast accept/edit/reject with source context and undo |
| Long grammar lectures | Interrupts retrieval and overloads mobile UI | One concise actionable point plus optional detail |
| Binary wrong/right for open answers | Distrust and discouragement | Correct/acceptable/partial/incorrect/uncertain with evidence |
| Reveal treated as success | Inflated mastery | Record reveal/assistance and schedule accordingly |
| Hidden generation failure | Spinner appears frozen | Durable progress steps, timeout guidance, retry, preserved lesson |
| Source disappears during feedback | Learner cannot verify AI judgment | Easy access to original sentence/source occurrence |
| Automatic difficulty with no explanation | Learner loses control | Show why an item is due and allow easy/difficult/mastered input |
| Exercise renderer inconsistency | Every module feels like a different app | Shared session shell, answer/submit/feedback contracts, design tokens |

## “Looks Done But Isn’t” Checklist

- [ ] **Module host:** A new proof exercise is added without a core-domain change and passes category conformance tests.
- [ ] **Analysis:** Restart the API/worker mid-job; the lesson survives and the job resumes or fails recoverably without duplicates.
- [ ] **Source integrity:** Editing a lesson does not silently rebind old units/exercises to the new source revision.
- [ ] **Structured output:** Valid-schema but invalid-source spans are rejected by domain validation.
- [ ] **Semantic evaluation:** A human-labeled corpus covers valid paraphrase, meaning drift, grammar-only error, missing target chunk, adversarial text, and uncertainty.
- [ ] **Attempts:** Retry, reveal, and assisted success remain distinct immutable records.
- [ ] **Review:** Every due item can explain its target units and scheduling evidence.
- [ ] **Provider outage:** Existing lessons, attempt history, and due review remain usable.
- [ ] **SQLite:** Fresh migration, concurrent job/session writes, restart, checkpoint, and backup/restore are tested.
- [ ] **Docker:** A fresh clone and fresh volume reach healthy state with one documented command.
- [ ] **Responsive UI:** Primary flow passes desktop Chromium, mobile Chromium, and mobile WebKit projects.
- [ ] **Deletion/privacy:** Lesson deletion behavior and AI metadata retention are explicit and verified.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Core-module coupling | HIGH | Freeze feature work, map forbidden imports/switches, extract ports, add conformance suite, migrate modules one category at a time |
| Missing provenance | HIGH | Introduce source revisions/run records, backfill only trustworthy links, mark unverifiable artifacts stale |
| Lost/duplicate jobs | MEDIUM | Add idempotency and job state, reconcile duplicate outputs by run/source keys, expose retry |
| Bad semantic grades | MEDIUM | Disable affected prompt/model version, mark results, expand labeled corpus, recalibrate and re-evaluate where safe |
| SQLite contention | MEDIUM | Shorten transactions, serialize worker writes, tune timeout/checkpoint, then migrate adapter to PostgreSQL if thresholds persist |
| Prompt injection | HIGH | Disable affected AI feature, rotate exposed secrets, inspect traces, harden separation/validation, add regression attacks |

## Pitfall-to-Roadmap Mapping

| Pitfall | Prevention Stage | Verification |
|---------|------------------|--------------|
| Paper-only modules | Contracts/module-host foundation | Proof module + forbidden-import checks + conformance suite |
| Lost provenance | Lesson/analysis vertical slice | Revision/edit/retry integration tests |
| Request-bound AI | Analysis job foundation | Restart/idempotency/failure E2E tests |
| False AI confidence | AI evaluation foundation | Human-calibrated regression corpus and uncertainty cases |
| Bad grading semantics | Exercise/evaluation phases | Per-exercise rubrics and paraphrase/meaning-drift cases |
| Weak scheduler evidence | Attempt then review phases | Reveal/retry/unit-link scheduling tests |
| SQLite operational gaps | Persistence foundation and hardening | Concurrency, WAL, backup/restore, migration tests |
| Prompt injection | Provider/feature foundation | Adversarial source suite and sanitized rendering test |
| English leakage | Language capability foundation | Import rule plus Unicode/non-Latin fixtures |
| Shrunk-desktop UI | Shell and each exercise slice | Playwright desktop/mobile/WebKit acceptance |

## Sources

- [SQLite WAL documentation](https://www.sqlite.org/wal.html) — concurrency, same-host limitation, checkpoint starvation, and WAL growth.
- [FastAPI background-task caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/) — limits of request-adjacent background work.
- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — untrusted-content separation, least privilege, filtering, and monitoring.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — external-content segregation, privilege control, and adversarial testing.
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — schema adherence and typed parsing.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — continuous task-specific evals and human calibration.
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) — red teaming, human oversight, source access, and input limits.
- [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — running versus healthy dependencies.
- [Playwright emulation](https://playwright.dev/docs/emulation) — mobile/touch/browser emulation.
- `docs/prd/PRD.md` — product-specific risks and mitigations.

---
*Pitfalls research for: AI Language Coach*
*Researched: 2026-07-15*
