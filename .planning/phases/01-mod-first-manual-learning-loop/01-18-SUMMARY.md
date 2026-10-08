---
phase: 01-mod-first-manual-learning-loop
plan: 18
revision: 2
subsystem: ui
tags: [react, inline-feedback, disclosure, saved-feedback, restoration, docker]
requires:
  - phase: 01-17
    provides: "Complete real saved feedback through SQLite, query, HTTP and generated client"
provides:
  - "Single inline accepted/wrong/revealed result with clearing retry and no duplicate graded input/card"
  - "Exact saved attempt/item-bound restoration and disclosure with stale-response guards"
  - "Explicit Phase 1 scope narrowing and approved repeated Docker human checkpoint"
affects: [phase-01-verification, phase-05-feedback, EVAL-05]
actuals:
  tokens: null
  tasks: 3
  commits: 0
actuals_note: "No reliable combined R1/R2 clean diff baseline is asserted here; token estimate omitted rather than attributing pre-existing edits."
plan_head_before: a2220b13a4abf4d7986df08a915b380a39f4782b
plan_head_after: a2220b13a4abf4d7986df08a915b380a39f4782b
tech-stack:
  added: []
  patterns:
    - "Result displayed in the original gap; deferred education stays in the real saved payload"
    - "Versioned local identity/prompt/reveal binding; saved attempt remains authoritative"
key-files:
  created:
    - .planning/phases/01-mod-first-manual-learning-loop/01-18-SUMMARY.md
  modified:
    - frontend/src/registries/renderers/GapFillRenderer.tsx
    - frontend/src/registries/renderers/GapFillRenderer.module.css
    - frontend/src/registries/renderers/gapFillRenderer.test.tsx
    - frontend/src/registries/renderers/types.ts
    - frontend/src/features/lesson/stageState.ts
    - frontend/src/features/lesson/LessonWorkspacePage.tsx
    - frontend/src/features/lesson/LessonWorkspacePage.test.tsx
    - frontend/src/features/lesson/FocusPracticeMode.test.tsx
key-decisions:
  - "D-32–D-37 supersede the not-approved R1 Details presentation; original full EVAL-05 stays partial/deferred."
  - "Correct/Corrected fills accepted reference once in green; Incorrect hides reference until Show answer."
  - "Try again clears before and after reveal without changing domain retry, score or Exit rules."
  - "All real saved educational fields and durable restoration fixes remain, despite deferred display."
  - "Detailed education belongs to Phase 5; multi-blank/true drag-and-drop is future work only."
patterns-established:
  - "No fabricated feedback defaults on reopen; strict payload validation and exact copy/attempt binding"
requirements-completed: []
requirements-addressed: [EVAL-05, EVAL-01, EXER-07]
requirement-closure: "Narrowed Phase 1 behavior approved; original full EVAL-05 not complete. Separate phase smoke and re-verification pending."
coverage:
  - id: D1
    description: "Inline accepted/wrong/revealed result, clearing Try again, no duplicate graded input/card/Details"
    requirement: EVAL-05
    verification:
      - kind: automated_ui
        ref: "frontend/src/registries/renderers/gapFillRenderer.test.tsx"
        status: pass
      - kind: manual_procedural
        ref: ".planning/phases/01-mod-first-manual-learning-loop/01-18-CHECKPOINT.md#t3--approved-human-verification-checklist"
        status: pass
    human_judgment: true
    rationale: "Docker learner-visible states and 320px wrap require human judgment; user explicitly approved R2 without observations."
  - id: D2
    description: "Actual saved educational payload and exact attempt/item-bound state survive reopen without stale disclosure"
    requirement: EVAL-05
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
      - kind: integration
        ref: "backend/tests/adapters/http/test_http_dto_mapping.py"
        status: pass
      - kind: manual_procedural
        ref: ".planning/phases/01-mod-first-manual-learning-loop/01-18-CHECKPOINT.md#dockerdata-preservation"
        status: pass
    human_judgment: true
    rationale: "Published four-state/five-route checklist approved by user report; automated payload digest independently proves data preservation, not visual restoration."
  - id: D3
    description: "Existing retry rounds, corrected exclusion, Continue, opening score, Start Over and Exit retained"
    requirement: EXER-07
    verification:
      - kind: automated_ui
        ref: "frontend/src/features/lesson/FocusPracticeMode.test.tsx"
        status: pass
      - kind: integration
        ref: "backend/tests/application/test_practice_retry.py"
        status: pass
      - kind: manual_procedural
        ref: ".planning/phases/01-mod-first-manual-learning-loop/01-18-CHECKPOINT.md#t3--approved-human-verification-checklist"
        status: pass
    human_judgment: true
    rationale: "User approved the R2 checklist including frozen learner workflow; this is not phase-wide smoke approval."
duration: "Not measured; combined R1/R2 execution includes human wait"
completed: 2026-10-07
human_approval: approved
human_approval_source: user_report
status: complete
---

# Phase 01 Plan 18 R2: Inline Feedback and Durable Restoration

Correct/Corrected now fills the accepted phrase once in the original blank, in green. Incorrect keeps the solution hidden until Show answer; Try again clears the result before or after reveal. No Details, technical chunk labels, separate answer card or duplicate graded input remain.

The user approved the repeated Docker checkpoint on 2026-10-07: “ручная проверка пройдена без замечаний approved.” All three plan tasks are complete. This is approval of the published R2 checklist as a whole, recorded as user-reported evidence; no assistant-observed route actions or per-route screenshots are claimed. R1 remains explicitly not approved.

## Accomplishments and scope

- R2 revised the renderer/CSS and test contracts to the agreed single-blank UX. No LLM or new explanation templates were introduced in R2.
- Retained R1/01-17 production fixes: complete saved explanation/chunks/nullable alternative, exact session/attempt/unit/item/retry-copy binding, versioned reveal, pending final success before Continue, strict history errors and late-response guards. Rich original content is asserted at the renderer seam even though education is intentionally not displayed.
- Incorrect retry clears local response/result/reveal without a domain mutation. Existing same-session retry rounds, corrected exclusion, score denominator, Continue, Start Over and Exit remain unchanged.
- D-32–D-37 explicitly narrow Phase 1. Original full EVAL-05 is **not implemented in full**: detailed teaching, chunk analysis and optional alternative presentation are deferred to Phase 5. Shared multi-blank exercise and actual drag-and-drop are recorded only in 01-18-FOLLOWUPS.md as proposed Phase 4/9 work.

## Verification evidence

These are the previously completed implementation checks, not new executions during approval recording:

| Check | Result |
| --- | --- |
| R2 renderer RED before production edit | 10 failed / 6 passed; old Details/duplicate UI, missing inline state and post-reveal retry exposed |
| Renderer GREEN and tracer rerun | 16 passed each |
| Workspace / Focus / FeedbackStage target | 69 passed, including 59 workspace tests |
| Full frontend | 105 passed, 9 files |
| Full backend | 129 passed, no skipped; pre-existing Starlette/httpx deprecation warning |
| Frontend typecheck / production build | Passed |
| R2 plan structure / decision coverage | Valid 3 tasks; D-32–D-37 6/6; inline review, not independent-agent review |
| Docker rebuild/restart, volume retained | API healthy, web HTTP 200; current production assets served |
| Repeated final T3 checkpoint | Approved by user, no observations |

Docker `up -d --build --wait api web` and `restart api web` retained the volume. All 188 full attempt payloads in the captured R2 read-only baseline remained identical after restart: 152 nonempty used arrays and 36 nonempty missed arrays. SHA256: `E6E8B582FB72B561867F3E3C6844E75D40AA3CD7BDE58DFB93130205D5F70B6B`. No user-data writes, SQL edits, seeding or volume deletion were performed by the assistant. Published hidden/revealed/correct/corrected × five entry/restart routes are approved by user report in the checkpoint matrix.

## Deviations, issues and observations

R1 Details presentation was not approved and was superseded by explicit user-directed R2 scope narrowing. R2 changed rendering/tests, not the saved-data or restore production fixes. Parameterless Try again wrapping prevents event arguments leaking into the callback. No new dependencies, provider calls, skipped behavioral tests or synthetic feedback defaults were added.

The user reported no observations for R2, so no new bug/UX/visual/workflow item requires classification. Education and multi-blank/drag-and-drop remain explicitly deferred, not silently counted as delivered. Historical R1 evidence is preserved in 01-18-CHECKPOINT-R1.md.

## Task Commits

T1, T2, T3 and metadata were uncommitted when the plan/checkpoint completed; earlier user instructions prohibited Git mutations. Execution actuals and before/after HEAD fields above describe that plan-time boundary, not the subsequent Git handoff. The user then explicitly answered Да to commit/push now. A scoped aggregate commit is authorized on `phase/01-execution`; its actual hash/push result belong to Git history and the handoff, without rewriting these historical task actuals.

Pre-commit checks rerun after that authorization: full backend 129 passed, full frontend 105 passed and typecheck passed. No production/test edits since the approved Docker checkpoint. Forty-two relevant files are selected; five pre-existing historical audit artifacts are excluded and preserved locally.

## User Setup Required

None for the completed plan.

## Next Gate

All 18 Phase 1 plans are complete, but Phase 1 remains open. Next is a **separate phase-wide Docker learner-flow smoke and re-verification under D-32–D-37**, recorded in 01-VALIDATION.md. Per-plan approval does not satisfy that gate, close original full EVAL-05, authorize Phase 2, or authorize phase.complete. PLAT-09 remains closed and needs no new gap plan.

## Self-Check

Checkpoint approval, summary, validation, requirement traceability and plan counts reconciled. No source changes or automated suite rerun in the approval-recording turn. `git diff --check` passed, staged diff is empty and `git rev-list --count a2220b13a4abf4d7986df08a915b380a39f4782b..HEAD` is 0. Summary frontmatter validated after adding the required duration field; active time was not measured and is not invented. No fabricated task commit hashes or full-requirement closure.
