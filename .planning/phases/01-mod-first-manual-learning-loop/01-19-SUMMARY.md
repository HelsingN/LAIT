---
phase: 01-mod-first-manual-learning-loop
plan: 19
subsystem: persistence
status: complete
tags: [sqlite, concurrency, retry, append-only, regression]
requires:
  - phase: 01-18
    provides: "Approved inline feedback and exact saved-attempt restoration"
provides:
  - "Delayed and replayed submits preserve authoritative durable progression"
  - "Serialized final-position advancement appends one retry round"
  - "Late submit losing to Exit cannot append to closed history"
affects: [phase-01-verification, EXER-02, EXER-07]
actuals:
  tokens: null
  tasks: 2
  commits: 1
actuals_note: "One production commit; documentation commits tracked separately. No reliable token or wall-time measurement claimed."
plan_head_before: d8b2611
plan_head_after: d6abcc6
tech-stack:
  added: []
  patterns:
    - "Database open-session write lock before reading/checking progression"
    - "Attempt insertion does not assign a cursor captured by the handler"
key-files:
  created:
    - .planning/phases/01-mod-first-manual-learning-loop/01-19-PLAN.md
    - .planning/phases/01-mod-first-manual-learning-loop/01-19-PLAN-CHECK.md
    - .planning/phases/01-mod-first-manual-learning-loop/01-19-SUMMARY.md
  modified:
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/application/commands/exercise_submit_attempt.py
    - backend/tests/application/test_practice_retry.py
key-decisions:
  - "Keep add_attempt compatibility signature but ignore stale cursor; every accepted request still gets a distinct attempt."
  - "Serialize through the database, not a process-only mutex; recheck open status under the write lock."
  - "Guard progression by captured position and return actual persisted cursor when no advancement is required."
  - "No UI, schema, DTO, retry/category or learner-data changes; original EVAL-05 remains deferred to Phase 5."
requirements-completed: [EXER-02, EXER-07]
requirements-addressed: [EXER-02, EXER-07]
coverage:
  - id: D1
    description: "Delayed incorrect/correct request captured at 0 returns and persists cursor 2, including a new repository"
    requirement: EXER-02
    verification:
      - kind: integration
        ref: "backend/tests/application/test_practice_retry.py::test_delayed_submit_preserves_position_two_after_repository_reopen"
        status: pass
    human_judgment: false
  - id: D2
    description: "Replay retains distinct attempts; overlapping final Continue appends one missed round; Exit protects closed history"
    requirement: EXER-07
    verification:
      - kind: integration
        ref: "backend/tests/application/test_practice_retry.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "Existing retry, pair identity, Corrected, denominator, Continue, Start Over, Exit and exact payload restoration remain green"
    requirement: EXER-07
    verification:
      - kind: integration
        ref: "01-VALIDATION.md#wr-02-gap-closure--2026-10-08"
        status: pass
      - kind: automated_ui
        ref: "frontend/src/features/lesson/LessonWorkspacePage.test.tsx"
        status: pass
    human_judgment: false
---

# Plan 01-19 — WR-02 ordered persistence

Completed the only newly authorized plan. Plans 01-01–01-18 were not re-executed.

## Task results

1. Added deterministic public-handler regressions against migrated temporary SQLite. RED on old code: four failures (delayed Incorrect 2→0, delayed Correct 2→1, duplicate final retry insert, late attempt retained after Exit), one replay case already passing. Added cursor-neutral attempt insertion, database-serialized progression and an authoritative response cursor. GREEN: retry file 9/9, including both delayed outcomes and fresh database reads of exactly 2. Production commit: `d6abcc6`.
2. Affected backend regression group 48/48; frontend Focus/Workspace/Feedback 69/69. Original standalone probe now 2→2, exit 0. Ruff check/format and git diff whitespace check passed. Final canonical verification is regenerated after these checks; historical 4/5 WR-02 report retained under verification-evidence.

## Behavior preserved

Accepted requests remain append-only, including replays. Earlier attempt rows are compared unchanged; named item/pair identity and the opening denominator remain intact. Late writes rejected because Exit already won are not accepted attempts. Corrected/retry/Continue/Start Over/Exit rules and saved educational fields are unchanged. No request deduplication, new schema/transport field, new dependency or learner database write.

## Verification limits and deviations

Backend-only implementation needs no new blocking-human UI checkpoint. Retain current UAT 76/76 (14 human reports + 62 recorded automated checks) and the already completed Docker phase smoke; no fresh human/browser/Docker observation is claimed. The affected 57 backend + 69 frontend tests are not a fresh full-suite run. PostgreSQL locking behavior is not runtime-tested here; production SQLite is exercised with separate connections and a fresh repository. Full EVAL-05 education stays partial/deferred to Phase 5.

Raw UAT-HISTORY bytes and old failed rows remain untouched. The CLI archive-discovery false positive is administrative debt before a later phase transition; no force bypass, phase.complete or push.

## Threat Flags

T-01-51 closed by cursor-neutral insertion, serialized open-session write and deterministic race/replay/Exit regressions. No open blocking threat introduced.

## Self-Check: PASSED

Three intended backend files committed; both tasks complete; fresh affected checks green; no completed plan rerun. Canonical verification/fingerprint and state tracking are the closeout evidence.
