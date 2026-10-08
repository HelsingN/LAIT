---
phase: 01-mod-first-manual-learning-loop
plan: 03
subsystem: api
tags: [fastapi, sqlalchemy, alembic, sqlite, learning-unit]

requires:
  - phase: 01-01
    provides: lesson.create persistence and D-23 handler boundary
provides:
  - learning_unit.add stores an exact Unicode code-point span as a draft
  - learning_unit.accept moves a draft into the accepted pool
  - learning_unit.remove logically deletes via removed_at and allows re-add as a new id
  - learning_unit.list returns live draft and accepted units
  - HTTP DTO routes with stable operationIds, registered without editing app.py
affects: [01-04, 01-05, 01-06]

actuals:
  tokens: 12411
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns:
    - logical delete via removed_at
    - span offsets as Python str indices
    - reject_if_unit_set_frozen before unit writes
    - RepositoryBundle on the existing open_repository object

key-files:
  created:
    - backend/lait/domain/span.py
    - backend/lait/domain/learning_unit.py
    - backend/lait/application/commands/learning_unit_add.py
    - backend/lait/application/commands/learning_unit_accept.py
    - backend/lait/application/commands/learning_unit_remove.py
    - backend/lait/application/commands/unit_set_freeze.py
    - backend/lait/application/queries/learning_unit_list.py
    - backend/lait/adapters/persistence/repositories.py
    - backend/lait/adapters/http/routers/learning_units.py
    - backend/alembic/versions/20261001_0002_create_learning_units.py
  modified:
    - backend/lait/application/ports.py
    - backend/lait/adapters/persistence/models.py
    - backend/lait/adapters/persistence/database.py
    - backend/lait/adapters/http/routers/__init__.py

key-decisions:
  - "learning_unit.remove sets removed_at and keeps the row; re-add inserts a new id"
  - "Source span offsets are Unicode code points, Python str indices, in persistence and HTTP"
  - "add, remove, and accept call reject_if_unit_set_frozen, which asks has_open_practice_session and gets false until plan 01-05"
  - "The lesson foreign key is ON DELETE RESTRICT. This plan creates no ON DELETE CASCADE"
  - "Unit HTTP routes register beside lessons. app.py is unchanged"

patterns-established:
  - "Pattern: overlap is start < other.end and other.start < end, skipping removed_at rows"
  - "Pattern: unit commands reject a frozen set before any write"
  - "Pattern: routers map DTOs onto handlers and read the repository from app.state"

requirements-completed: [ANLY-08]

coverage:
  - id: D1
    description: "learning_unit.add stores a draft whose text equals the selected source span"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_add_stores_exact_span_text_as_draft"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_missing_span_writes_no_row"
        status: pass
    human_judgment: false
  - id: D2
    description: "Overlapping spans are rejected and the existing unit stays; touching edges create two units"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/domain/test_spans.py#test_overlapping_spans_are_rejected_by_predicate"
        status: pass
      - kind: unit
        ref: "backend/tests/domain/test_spans.py#test_touching_edges_do_not_overlap"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_overlap_of_rolling_out_keeps_existing_unit"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_touching_edges_create_two_units"
        status: pass
    human_judgment: false
  - id: D3
    description: "Accept moves a draft to accepted and list returns both live units"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_accept.py#test_accept_flips_draft_and_list_returns_both"
        status: pass
    human_judgment: false
  - id: D4
    description: "Logical remove keeps the row, hides it from list, and re-add of the same span inserts a new id"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_remove_sets_removed_at_and_keeps_the_row"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_logical_removed_span_can_be_readded_as_new_unit"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_same_phrase_in_two_places_creates_two_units"
        status: pass
    human_judgment: false
  - id: D5
    description: "Canonical offsets are Unicode code points. UTF-16 offsets past the source are rejected"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_add.py#test_offsets_are_unicode_code_points_not_utf16"
        status: pass
      - kind: integration
        ref: "backend/tests/application/test_learning_unit_add.py#test_http_maps_learning_unit_dtos"
        status: pass
    human_judgment: false
  - id: D6
    description: "A frozen port rejects add, remove, and accept before any write. The real port reports not frozen"
    requirement: ANLY-08
    verification:
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_add_without_row_change"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_remove_without_row_change"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_accept_without_row_change"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_not_frozen_port_allows_add"
        status: pass
    human_judgment: false
  - id: D7
    description: "HTTP routes map DTOs onto the handlers with stable operationIds and do not edit app.py"
    requirement: ANLY-08
    verification:
      - kind: integration
        ref: "backend/tests/application/test_learning_unit_add.py#test_http_maps_learning_unit_dtos"
        status: pass
      - kind: unit
        ref: "backend/tests/application/test_learning_unit_remove.py#test_learning_unit_migration_does_not_cascade_deletes"
        status: pass
    human_judgment: false

duration: 48min
completed: 2026-10-01
status: complete
plan_head_before: 6f211b470598dae11c8d117b75dda0b56f9c20a8
plan_head_after: f06b7cc8f5baf4e3a90eb91d9b827a976be27d82
---

# Phase 1 Plan 03: Manual Learning Units Summary

**Exact source-span drafts with accept, logical remove, and re-add of a removed span as a new id, behind D-23 handlers and DTO-only HTTP routes**

## Performance

- **Duration:** 48 min
- **Started:** 2026-10-01T05:34:00Z
- **Completed:** 2026-10-01T06:22:00Z
- **Tasks:** 3
- **Files modified:** 18

## Accomplishments

- `learning_unit.add` stores a draft whose text is `source[start:end]` in Unicode code points. An empty or out-of-range selection writes no row.
- Overlap of `responsible for rolling out` with `rolling out` is rejected and the existing unit stays. Touching edges and the same phrase in two places are two units.
- `learning_unit.remove` sets `removed_at` and keeps the row. List hides it. Adding that span again inserts a new id. The lesson foreign key is `ON DELETE RESTRICT`.
- `learning_unit.add`, `learning_unit.remove`, and `learning_unit.accept` call `reject_if_unit_set_frozen` before any write. `has_open_practice_session` returns false until plan 01-05.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end add span → accept → list** - `b1098cf` (test, RED) then `ce0b568` (feat, GREEN)
2. **Task 2: Expand remove + same-phrase-two-places** - `5215a4e` (test, RED) then `e1f825f` (feat, GREEN)
3. **Task 3: HTTP DTO wiring for unit commands** - `f06b7cc` (feat)

**Deviation fix:** `035bdb2` (fix: freeze helper docstring)

**Plan metadata:** docs commit containing this summary

## Files Created/Modified

- `backend/lait/domain/span.py` - overlap predicate; touching edges are disjoint
- `backend/lait/domain/learning_unit.py` - draft/accepted unit and span errors
- `backend/lait/application/commands/learning_unit_add.py` - exact-span capture
- `backend/lait/application/commands/learning_unit_accept.py` - draft to accepted
- `backend/lait/application/commands/learning_unit_remove.py` - logical delete
- `backend/lait/application/commands/unit_set_freeze.py` - freeze gate over the repository port
- `backend/lait/application/queries/learning_unit_list.py` - live units only
- `backend/lait/adapters/persistence/repositories.py` - SQLite unit store; `has_open_practice_session` returns false
- `backend/lait/adapters/http/routers/learning_units.py` - DTO mapping and operationIds
- `backend/alembic/versions/20261001_0002_create_learning_units.py` - `learning_units` table, `ON DELETE RESTRICT`

## Decisions Made

- Remove is a logical delete. Re-add does not revive the removed row.
- Offsets stored and accepted by HTTP are Python `str` indices. The API does not take DOM UTF-16 offsets.
- Freeze is an application-command call to `has_open_practice_session`. Routers do not enforce it.
- `open_repository` returns a bundle that implements lesson and unit ports, so `app.py` stays unchanged.
- No `ON DELETE CASCADE` in this revision. Future `Attempt.learning_unit_id` stays `ON DELETE RESTRICT`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Unit persistence is reached through the existing repository object**
- **Found during:** Task 1 (End-to-end add span → accept → list)
- **Issue:** `create_app` only stores `lesson_repository`, and this plan must not edit `app.py`. A separate unit repository would be unreachable from HTTP.
- **Fix:** `RepositoryBundle` implements both ports. `open_repository` returns it. `LearningUnitRepository` was added to `ports.py`.
- **Files modified:** `backend/lait/adapters/persistence/database.py`, `backend/lait/adapters/persistence/repositories.py`, `backend/lait/application/ports.py`
- **Verification:** lesson tests still pass; unit handlers persist through the same object; `app.py` has no diff in this plan
- **Committed in:** `ce0b568` (Task 1 GREEN)

**2. [Rule 1 - Bug] Freeze helper docstring tripped the application import scan**
- **Found during:** Task 3 (HTTP DTO wiring)
- **Issue:** `test_application_handlers_do_not_import_fastapi_or_sqlalchemy` flags the substring `sqlalchemy`. The freeze module docstring named `SqlAlchemyLearningUnitRepository`.
- **Fix:** Reworded the docstring so the application package does not contain that substring.
- **Files modified:** `backend/lait/application/commands/unit_set_freeze.py`
- **Verification:** `test_application_handlers_do_not_import_fastapi_or_sqlalchemy` passes
- **Committed in:** `035bdb2`

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** Both keep the locked boundaries: `app.py` unchanged, handlers free of persistence imports. No scope creep.

## Authentication Gates

None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

| File | Line | Reason |
|------|------|--------|
| `backend/lait/adapters/persistence/repositories.py` | 80 | `has_open_practice_session` returns false until plan 01-05 binds an open PracticeSession. Intentional. |

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 add/accept/list | `b1098cf` `RED_EVIDENCE_OK` / `target_test_failed` for `test_add_stores_exact_span_text_as_draft` | `ce0b568` | — | Pass |
| 2 remove/re-add/freeze | `5215a4e` `RED_EVIDENCE_OK` / `target_test_failed` for `test_logical_removed_span_can_be_readded_as_new_unit` | `e1f825f` | — | Pass |
| 3 HTTP DTOs | not behavior-TDD (`type="auto"`) | `f06b7cc` | — | Pass |

## Threat Flags

None. The new unit routes are the planned client-to-command boundary. Offsets are checked against the source, and overlap is recomputed from live rows.

## Next Phase Readiness

- Ready for 01-04. Accepted units are the pool Gap Fill will read. Drafts stay out of that pool via `status`.
- Plan 01-05 replaces `has_open_practice_session` and must not edit the three unit command modules.
- ANLY-08 is also declared by plan 01-06, so the requirement checkbox stays open until that plan finishes.

## Self-Check: PASSED

- FOUND: `backend/lait/domain/span.py`
- FOUND: `backend/lait/application/commands/learning_unit_remove.py`
- FOUND: `backend/lait/adapters/http/routers/learning_units.py`
- FOUND: `backend/tests/application/test_learning_unit_remove.py`
- FOUND: `b1098cf`
- FOUND: `ce0b568`
- FOUND: `5215a4e`
- FOUND: `e1f825f`
- FOUND: `035bdb2`
- FOUND: `f06b7cc`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
