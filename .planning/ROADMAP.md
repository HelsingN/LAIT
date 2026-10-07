# Roadmap: AI Language Coach

## Overview

This roadmap grows the product through vertical MVP slices that keep the learning workflow usable while proving the Mod-First architecture in real use. It begins with a local manual learning loop over public contracts, then adds durable AI-assisted learning-unit review, progressively harder exercise modules, trustworthy semantic evaluation, scheduled review, resilient lesson lifecycle behavior, extension-contract parity, and finally responsive operational hardening of the complete lesson-to-review workflow.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Mod-First Manual Learning Loop** - Run locally, paste a lesson, add a learning unit, and complete a Gap Fill exercise through public module contracts.
- [ ] **Phase 2: AI-Assisted Learning-Unit Review** - Analyze a source through durable AI jobs and review source-grounded candidate learning units without breaking the manual loop.
- [ ] **Phase 3: Assisted Chunk Retrieval** - Add normalized Chunk Completion practice with retry, reveal, source inspection, and preserved Unicode content.
- [ ] **Phase 4: Resumable Sentence Reconstruction** - Add Sentence Reconstruction and let learners resume interrupted progressive-retrieval sessions.
- [ ] **Phase 5: Trustworthy Keyword Recall** - Complete the four-exercise progression with semantic evaluation, uncertainty, overrides, safe feedback, and quality calibration.
- [ ] **Phase 6: Weak-Unit Review Loop** - Turn attempt evidence into an explainable due-review queue whose outcomes influence future scheduling.
- [ ] **Phase 7: Resilient Lesson Lifecycle** - Let learners evolve, archive, restore, and delete lessons while preserving revision history and surviving AI outages safely.
- [ ] **Phase 8: Public Contract Parity** - Prove bundled and proof-of-concept modules conform to versioned public contracts, storage ownership, and compatibility rules.
- [ ] **Phase 9: Responsive Local Release** - Validate the complete workflow on desktop and mobile with durable storage, bounded performance, browser coverage, and recoverable operations.

## Phase Details

### Phase 1: Mod-First Manual Learning Loop

**Goal:** A learner can launch the local application and complete a source-to-feedback Gap Fill workflow, while maintainers can observe that it runs through documented public contracts.
**Mode:** mvp
**Depends on:** Nothing (first phase)
**Requirements:** LESS-01, LESS-02, ANLY-08, EXER-01, EXER-02, EXER-03, EXER-07, EVAL-01, EVAL-04, EVAL-05, MODL-01, MODL-02, MODL-03, MODL-12, PLAT-03, PLAT-09, PLAT-10
**Success Criteria** (what must be TRUE):
  1. Learner can start the health-checked application with Docker Compose, paste English text into a lesson, and reopen that lesson from the local lesson list.
  2. Learner can manually add and accept a source-linked learning unit, generate a Gap Fill exercise from it, and complete the exercise one item at a time.
  3. Learner receives deterministic Correct/Incorrect/Corrected feedback and Continue within the session. Correct/Corrected fills the current blank with the accepted phrase in green; Incorrect shows submitted inline without the solution, Show answer fills the reference, and Try again clears the response before/after reveal. No separate answer card, duplicate graded input, Details or technical chunk labels. Full real saved payload and exact attempt/item-bound restore/reveal remain intact across entry/restart paths; retry rounds, score and Exit are unchanged. Approved scope narrowing D-32–D-37 defers detailed educational explanation/chunk/alternative presentation to Phase 5: original full EVAL-05 is not completed by Phase 1. No LLM or new explanation templates in Phase 1.
  4. Maintainer can inspect active modules and capabilities, invoke the workflow through documented commands and queries, add a proof exercise contribution through the public registry and renderer seams without changing core domain services, and see startup reject invalid or incompatible module catalogs.
  5. Maintainer can generate the TypeScript client from OpenAPI, have CI detect an unreviewed contract/client mismatch, and test the core, persistence adapter, and bundled modules independently.

**Plans:** 18 plans — all executed; 01-18 R2 checkpoint approved, separate phase smoke/re-verification pending

Plans:
- [x] 01-01-PLAN.md
- [x] 01-02-PLAN.md
- [x] 01-03-PLAN.md
- [x] 01-04-PLAN.md
- [x] 01-05-PLAN.md
- [x] 01-06-PLAN.md
- [x] 01-07-PLAN.md
- [x] 01-08-PLAN.md
- [x] 01-09-PLAN.md
- [x] 01-10-PLAN.md
- [x] 01-11-PLAN.md
- [x] 01-12-PLAN.md — Return the same-generation open session and resume it after reload
- [x] 01-13-PLAN.md — Restore a matching generation and attempts after reload, and end the pass on the last Continue
- [x] 01-14-PLAN.md — Widen the workspace and make preparation actions obvious
- [x] 01-15-PLAN.md — Close the five practice and feedback UX gaps from UAT G-01-1
- [x] 01-16-PLAN.md — Retry a miss in the same pass, then continue into still-uncorrected items

**Wave 12 — gap closure, executed after 01-16 (wave 11)**
- [x] 01-17-PLAN.md — Recover complete saved feedback through repository, query, HTTP and generated DTO

**Wave 13 — gap closure, automatic tasks green; final 01-18 R2 blocking-human Docker checkpoint approved 2026-10-07**
- [x] 01-18-PLAN.md — Revised inline result UX, retained exact feedback restoration and repeated final blocking-human Docker checkpoint (D-32–D-37; original EVAL-05 partial/deferred)

**Cross-cutting constraints:** Preserve real saved educational payload and item/attempt identity; no schema migration or retry/score/Exit changes. PLAT-09 is closed. Execution is explicitly authorized by execute-phase 01 --gaps-only; final R2 checkpoint approved by user without observations. Subsequent explicit Да authorizes scoped commit/push to the current branch, not phase closure. Separate phase Docker smoke/re-verification remains pending.

**UI hint:** yes

### Phase 2: AI-Assisted Learning-Unit Review

**Goal:** A learner can turn a preserved source revision into reviewed lexical learning units through a durable, transparent, and safely bounded AI workflow.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** LESS-07, ANLY-01, ANLY-02, ANLY-03, ANLY-04, ANLY-05, ANLY-06, ANLY-07, AIOP-01, AIOP-02, AIOP-03, AIOP-07, AIOP-09, AIOP-12, MODL-06, MODL-07, PLAT-06
**Success Criteria** (what must be TRUE):
  1. Learner can request analysis, keep using or reopen the application, and observe queued, running, completed, or recoverably failed status without duplicate candidates.
  2. Learner receives source-grounded chunks, collocations, phrasal verbs, and sentence patterns, can inspect each occurrence, and can accept, edit, reject, or undo rejection before exercise generation.
  3. Learner can inspect the immutable source revision behind every candidate and is told which configured provider may receive source text before the first transmission.
  4. Maintainer can replace either the OpenAI-compatible provider or the analysis feature independently, with validated outputs and trace records that distinguish retryable, permanent, refusal, and uncertain dispositions.
  5. Pasted text remains untrusted data separated from instructions and cannot grant model tools or application privileges.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 2`

**UI hint:** yes

### Phase 3: Assisted Chunk Retrieval

**Goal:** A learner can practice accepted units with Chunk Completion using English-owned normalization and explicit assistance evidence.
**Mode:** mvp
**Depends on:** Phase 2
**Requirements:** EXER-04, EXER-08, EXER-09, EVAL-02, EVAL-06, MODL-05, PLAT-05
**Success Criteria** (what must be TRUE):
  1. Learner can complete Chunk Completion exercises through the same session and exercise-registry contracts used by Gap Fill.
  2. Learner can retry after feedback or reveal the relevant source, and each action is retained as distinct assistance evidence rather than independent recall.
  3. Deterministic comparison follows language-module rules for whitespace, capitalization, punctuation, contractions, and accepted variants, while source and answer text remain intact UTF-8.
  4. Learner can inspect the relevant original source directly from feedback.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 3`

**UI hint:** yes

### Phase 4: Resumable Sentence Reconstruction

**Goal:** A learner can reconstruct progressively less-supported sentences and resume an interrupted practice session without losing progress.
**Mode:** mvp
**Depends on:** Phase 3
**Requirements:** EXER-05, EXER-10
**Success Criteria** (what must be TRUE):
  1. Learner can complete Sentence Reconstruction exercises supplied through the public Exercise Registry as part of the existing lesson session.
  2. Learner can leave or refresh an in-progress session and resume at the correct exercise with all prior submissions and progress intact.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 4`

**UI hint:** yes

### Phase 5: Trustworthy Keyword Recall

**Goal:** A learner can complete the full four-stage retrieval progression and receive evidence-linked semantic feedback that is safe, calibrated, and honest about uncertainty.
**Mode:** mvp
**Depends on:** Phase 4
**Requirements:** EXER-06, EXER-11, EVAL-03, EVAL-07, EVAL-08, EVAL-09, EVAL-10, AIOP-04, AIOP-08, AIOP-10, AIOP-11, PLAT-08
**Success Criteria** (what must be TRUE):
  1. Learner can progress through Gap Fill, Chunk Completion, Sentence Reconstruction, and Keyword Recall with decreasing cue levels recorded for every submission.
  2. Learner can submit a natural meaning-preserving Keyword Recall answer, have it saved before provider evaluation, and receive either supported feedback or an explicit uncertain/unable-to-evaluate result.
  3. Learner can flag or override a questionable AI judgment without erasing the original evaluation, and all model-generated feedback renders without executable active content.
  4. Maintainer can run semantic evaluation against a versioned human-curated corpus with a deterministic fake provider and inspect provider usage and estimated cost without exposing secrets to the browser or logs.
  5. Product validation demonstrates that at least 80% of generated exercises are usable after learning-unit review on the agreed sample.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 5`

**UI hint:** yes

### Phase 6: Weak-Unit Review Loop

**Goal:** A learner can revisit weak learning units through an explainable due queue and have each review outcome shape future scheduling.
**Mode:** mvp
**Depends on:** Phase 5
**Requirements:** REVW-01, REVW-02, REVW-03, REVW-04, REVW-05, REVW-06, REVW-07, REVW-08, MODL-08
**Success Criteria** (what must be TRUE):
  1. Learner can inspect a chronological history of all submissions, including retries and assisted attempts, with the targeted and weak learning units identified.
  2. Learner can open an explainable queue of due learning units whose order reflects correctness, failures, elapsed time, assistance, and self-rating through the public scheduler contract.
  3. Learner can complete a due-review exercise, rate it easy, difficult, or mastered, and observe the resulting review state affect future due work.
  4. Maintainer can inspect and recompute review state from recorded scheduler identity, version, parameters, inputs, and outcome; the plain-text importer and scheduler are registered through category-specific public contracts and can be replaced without changing core learning workflows.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 6`

**UI hint:** yes

### Phase 7: Resilient Lesson Lifecycle

**Goal:** A learner can safely evolve and manage lessons across source revisions and provider failures without losing historical learning evidence.
**Mode:** mvp
**Depends on:** Phase 6
**Requirements:** LESS-03, LESS-04, LESS-05, LESS-06, ANLY-09, AIOP-05, AIOP-06
**Success Criteria** (what must be TRUE):
  1. Learner can rename, archive, restore, and explicitly delete a lesson with clearly stated and consistently applied related-data behavior.
  2. Learner can edit source text, retain the previously analyzed source as an immutable revision, and explicitly re-analyze without replacing accepted units or historical exercises.
  3. Learner can retry eligible AI work without duplicating accepted learning units, exercises, or attempts.
  4. Learner retains access to lessons, learning units, attempts, feedback, and due-review data while the configured AI provider is unavailable.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 7`

**UI hint:** yes

### Phase 8: Public Contract Parity

**Goal:** Maintainers can prove the complete learning workflow and a proof module obey versioned public extension boundaries with explicit compatibility and storage ownership.
**Mode:** mvp
**Depends on:** Phase 7
**Requirements:** MODL-04, MODL-09, MODL-10, MODL-11
**Success Criteria** (what must be TRUE):
  1. Maintainer can run one conformance suite successfully against all four bundled exercise modules and a proof-of-concept exercise module.
  2. Maintainer can add and run the proof exercise module without core changes, private cross-module imports, or writes to another component's private storage.
  3. Maintainer can validate explicit extension API and schema versions, identify incompatible modules before startup, and follow recorded compatibility or migration notes.
  4. Core-owned and module-owned records remain separately governed, typed or schema-versioned, and migrated by their responsible components while the learner workflow remains functional.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 8`

**UI hint:** yes

### Phase 9: Responsive Local Release

**Goal:** A learner can reliably complete the entire lesson-to-review workflow on supported desktop and mobile browsers from a durable local installation.
**Mode:** mvp
**Depends on:** Phase 8
**Requirements:** PLAT-01, PLAT-02, PLAT-04, PLAT-07, PLAT-11, PLAT-12, PLAT-13
**Success Criteria** (what must be TRUE):
  1. Learner can complete the full lesson-to-review workflow at supported desktop and mobile widths using touch and the on-screen keyboard where applicable.
  2. A documented normal-size lesson produces a complete exercise set within five minutes under the reference provider and environment.
  3. SQLite data survives container restart, uses WAL with bounded writes and busy handling, and can be consistently backed up, restored, and migrated toward PostgreSQL without changing core contracts.
  4. Maintainer can verify fresh-volume startup, restart, interrupted AI work, concurrent session/job writes, migrations, and persisted data without manual database edits.
  5. Maintainer can run the primary workflow on Chromium plus targeted WebKit and mobile-emulation projects.

**Plans:** TBD

Plans:
- [ ] To be defined during `$gsd-plan-phase 9`

**UI hint:** yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Mod-First Manual Learning Loop | 18/18 | In Progress|  |
| 2. AI-Assisted Learning-Unit Review | 0/TBD | Not started | - |
| 3. Assisted Chunk Retrieval | 0/TBD | Not started | - |
| 4. Resumable Sentence Reconstruction | 0/TBD | Not started | - |
| 5. Trustworthy Keyword Recall | 0/TBD | Not started | - |
| 6. Weak-Unit Review Loop | 0/TBD | Not started | - |
| 7. Resilient Lesson Lifecycle | 0/TBD | Not started | - |
| 8. Public Contract Parity | 0/TBD | Not started | - |
| 9. Responsive Local Release | 0/TBD | Not started | - |

---
*Roadmap approved: 2026-07-16*
*Granularity: fine*
