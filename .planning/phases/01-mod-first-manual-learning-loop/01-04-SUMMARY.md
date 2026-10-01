---
phase: 01-mod-first-manual-learning-loop
plan: 04
subsystem: api
tags: [gap-fill, exercise-protocol, deterministic-eval, proof-module]

requires:
  - phase: 01-02
    provides: static catalog, visibility contributions, list_visible_for
  - phase: 01-03
    provides: accepted learning-unit spans as Unicode code points
provides:
  - Gap Fill generate blanks only the target span inside a terminator sentence window
  - Gap Fill evaluate grades drag by learning_unit_id and typed text by trim plus casefold
  - D-18 explanations with used or missed chunks and null natural_alternative
  - Persistable five-value result category; Gap Fill emits only correct or incorrect
  - Proof generate and evaluate on the same public types, visibility maintainer
affects: [01-05, 01-07, 01-09]

actuals:
  tokens: 6957
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns:
    - public exercise types in lait.domain.exercise
    - module generate(source, units) and evaluate(item, answer)
    - sentence window owned by exercise-gap-fill
    - drag identity on DragAnswer.learning_unit_id

key-files:
  created:
    - backend/lait/domain/exercise.py
    - backend/lait/modules/exercise_gap_fill/generate.py
    - backend/lait/modules/exercise_gap_fill/evaluate.py
    - backend/lait/modules/exercise_gap_fill/feedback.py
    - backend/lait/modules/exercise_gap_fill/sentence_window.py
    - backend/lait/modules/exercise_proof/generate.py
    - backend/lait/modules/exercise_proof/evaluate.py
  modified: []

key-decisions:
  - "Shared exercise types live in lait.domain.exercise so Gap Fill and proof implement one contract and core never names a module id"
  - "Drag grading compares learning_unit_id. Matching chip text with a different id is incorrect"
  - "Typed match is strip plus casefold on both sides. Internal space, punctuation, and apostrophes stay significant"
  - "RESULT_CATEGORIES keeps acceptable, partial, and uncertain. Gap Fill returns only correct or incorrect"
  - "The sentence window is the previous . ! ? or start through the next terminator or end, inside exercise-gap-fill"
  - "Proof evaluate is drag-identity plus exact typed equality, with its own one-line explanation, and does not import Gap Fill"

patterns-established:
  - "Pattern: generate returns GenerateResult.items ordered by span start then learning_unit_id, plus chip_unit_ids"
  - "Pattern: a blank segment is ______ and neighboring source text in the window stays literal"
  - "Pattern: Evaluation.natural_alternative is null in Phase 1"
  - "Pattern: proof tests import the proof package directly and do not call list_visible_for"

requirements-completed: [EXER-03, EVAL-01, EVAL-04, EVAL-05, MODL-03]

coverage:
  - id: D1
    description: "One accepted unit produces one Gap Fill item that blanks only the target span and keeps the rest of the sentence literal"
    requirement: EXER-03
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_one_accepted_unit_blanks_only_the_target_span"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_keeps_only_the_target_sentence"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_uses_start_and_end_when_no_terminator"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_honors_exclamation_and_question_marks"
        status: pass
    human_judgment: false
  - id: D2
    description: "Multiple units order by span start then learning_unit_id, each item blanks only its own span, and generate exposes chip candidate ids"
    requirement: EXER-03
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_items_order_by_span_start_then_learning_unit_id"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_equal_span_start_orders_by_learning_unit_id"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_two_units_in_one_sentence_blank_only_their_own_span"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_generate.py#test_generate_exposes_chip_candidate_unit_ids"
        status: pass
    human_judgment: false
  - id: D3
    description: "Drag is correct only when the submitted learning_unit_id matches, even if the chip text is identical"
    requirement: EVAL-01
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_drag_is_correct_when_submitted_learning_unit_id_matches"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_drag_is_incorrect_for_other_unit_id_even_when_text_matches"
        status: pass
    human_judgment: false
  - id: D4
    description: "Typed answers match after trimming ends and casefold only"
    requirement: EVAL-01
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_typed_match_strips_ends_and_ignores_case_only"
        status: pass
    human_judgment: false
  - id: D5
    description: "The persistable result category has five values and Gap Fill emits only correct or incorrect"
    requirement: EVAL-04
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_gap_fill_emits_only_correct_or_incorrect"
        status: pass
    human_judgment: false
  - id: D6
    description: "Explanations use the D-18 templates, natural_alternative is null, and a hit records used while a miss records missed"
    requirement: EVAL-05
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_feedback.py#test_correct_explanation_matches_d18_and_records_used"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_gap_fill/test_feedback.py#test_incorrect_explanation_matches_d18_and_records_missed"
        status: pass
    human_judgment: false
  - id: D7
    description: "Proof generate and evaluate satisfy the same public protocol as Gap Fill and core does not special-case either module id"
    requirement: MODL-03
    verification:
      - kind: unit
        ref: "backend/tests/modules/exercise_proof/test_contract.py#test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill"
        status: pass
      - kind: unit
        ref: "backend/tests/modules/exercise_proof/test_contract.py#test_core_does_not_special_case_exercise_module_ids"
        status: pass
    human_judgment: false

duration: 17min
completed: 2026-10-01
status: complete
plan_head_before: 4b7f82b586497dd16904087630f30a4ef0e4263d
plan_head_after: eb614138570a777603e8816e6b7bdccc4685ddea
---

# Phase 1 Plan 04: Gap Fill Generate and Evaluate Summary

**Gap Fill blanks one span per accepted unit, grades drag by unit id and typed text by trim plus casefold, and a proof module implements the same generate/evaluate contract**

## Performance

- **Duration:** 17 min
- **Started:** 2026-10-01T07:05:09Z
- **Completed:** 2026-10-01T07:22:30Z
- **Tasks:** 3
- **Files modified:** 11

## Accomplishments

- One accepted unit becomes one Gap Fill item. The sentence window runs from the previous `.` `!` `?` or the start through the next terminator or the end. Only the target span is `______`.
- Drag is correct only when `learning_unit_id` matches. The same chip text with another id is incorrect.
- Typed match is `strip().casefold()` on both sides. `Rolling out` matches `rolling out`. `rolling  out`, `rolling out.`, and `rolling out's` do not.
- Feedback uses the D-18 templates. `natural_alternative` is null. A hit stores the target chunk as used. A miss stores it as missed.
- `RESULT_CATEGORIES` is `correct|acceptable|partial|incorrect|uncertain`. Gap Fill returns only `correct` or `incorrect`.
- Proof `generate` / `evaluate` use the same public types, stay `visibility: maintainer`, and do not import Gap Fill. Core domain, application, adapters, and catalog do not mention either module id.

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end Gap Fill generate + evaluate one unit** - `f24c005` (test), `78de06d` (feat)
2. **Task 2: Expand multi-unit ordering and neighbor visibility** - `d08ed96` (test), `9ac0732` (feat)
3. **Task 3: Proof module contract-valid generate/evaluate** - `7f95e9b` (test), `eb61413` (feat)

## Files Created/Modified

- `backend/lait/domain/exercise.py` - public accepted unit, item, answers, evaluation, five-value category
- `backend/lait/modules/exercise_gap_fill/sentence_window.py` - terminator window
- `backend/lait/modules/exercise_gap_fill/generate.py` - one item per unit, own-span blank, chip ids
- `backend/lait/modules/exercise_gap_fill/evaluate.py` - drag identity and typed_match
- `backend/lait/modules/exercise_gap_fill/feedback.py` - D-18 templates and used/missed chunks
- `backend/lait/modules/exercise_proof/generate.py` - smallest contract-valid generate
- `backend/lait/modules/exercise_proof/evaluate.py` - drag identity and exact typed compare
- `backend/tests/modules/exercise_gap_fill/test_generate.py` - window, order, neighbor blanks, chips
- `backend/tests/modules/exercise_gap_fill/test_evaluate.py` - identity trap, typed edges, emitted categories
- `backend/tests/modules/exercise_gap_fill/test_feedback.py` - D-18 copy and chunk disposition
- `backend/tests/modules/exercise_proof/test_contract.py` - shared protocol, no learner-list lookup

## Decisions Made

- The public contract is `lait.domain.exercise`. Both modules import it. Core does not import either module package.
- `generate(source, units) -> GenerateResult` and `evaluate(item, answer) -> Evaluation` are the callable shape plan 01-05 can load from a bundled package the same way the catalog loads `contribution.py`.
- Chip bank rendering stays a session concern. Generate only exposes ordered `chip_unit_ids`.
- Proof explanations are not the D-18 Gap Fill templates. The shared assertion checks the `Evaluation` shape, drag identity, and a non-empty explanation.
- Abbreviations may split on `.` `!` `?`. That rule stays in the Gap Fill module.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added the shared exercise types in core domain**
- **Found during:** Task 1 (End-to-end Gap Fill generate + evaluate one unit)
- **Issue:** The plan required one public generate/evaluate contract for Gap Fill and proof, and forbade core special-casing module ids. No shared type module existed, and putting the types inside Gap Fill would make proof import a private package.
- **Fix:** Added `backend/lait/domain/exercise.py` with `AcceptedUnit`, `ExerciseItem`, `GenerateResult`, `DragAnswer`, `TypedAnswer`, `Evaluation`, and `RESULT_CATEGORIES`.
- **Files modified:** `backend/lait/domain/exercise.py`
- **Verification:** Both modules type-check against it, and `test_core_does_not_special_case_exercise_module_ids` passes
- **Committed in:** `78de06d` (Task 1 feat)

**2. [Rule 1 - Bug] Proof contract test read `function.__file__`**
- **Found during:** Task 3 (Proof module contract-valid generate/evaluate)
- **Issue:** After generate existed, `Path(proof_generate.__file__)` raised `AttributeError` because `__file__` lives on the module, not the function.
- **Fix:** Read the source with `inspect.getfile`.
- **Files modified:** `backend/tests/modules/exercise_proof/test_contract.py`
- **Verification:** `test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill` passes
- **Committed in:** `eb61413` (Task 3 feat)

---

**Total deviations:** 2 auto-fixed (1 missing critical, 1 bug)
**Impact on plan:** The shared types are the contract this plan required. The test fix only changes how the proof source is read. No session orchestration, MCP, or AI.

## TDD Gate Compliance

| Task | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| 1 Gap Fill one unit | `f24c005` `RED_EVIDENCE_OK` / `target_test_failed` for `test_one_accepted_unit_blanks_only_the_target_span` (exit 1, 10 failed) | `78de06d` | — | Pass |
| 2 Multi-unit order | `d08ed96` `RED_EVIDENCE_OK` / `target_test_failed` for `test_items_order_by_span_start_then_learning_unit_id` (exit 1, 4 failed) | `9ac0732` | — | Pass |
| 3 Proof contract | `7f95e9b` `RED_EVIDENCE_OK` / `target_test_failed` for `test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill` (exit 1, 1 failed) | `eb61413` | — | Pass |

Tracer task 1 was re-run after GREEN (`10 passed`) before the multi-unit tests were added.

## Authentication Gates

None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for `01-05`. Handlers can call `generate` / `evaluate` on a learner-visible module package without hard-coding `official.exercise.gap-fill`. Practice session persistence, pass sequencing, and HTTP are still that plan. Proof removal without core edits stays in `01-09`. The renderer stays in `01-07`.

EXER-03, EVAL-01, EVAL-04, EVAL-05, and MODL-03 stay open in REQUIREMENTS.md until the later plans that also declare them have summaries.

## Self-Check: PASSED

- FOUND: `backend/lait/domain/exercise.py`
- FOUND: `backend/lait/modules/exercise_gap_fill/generate.py`
- FOUND: `backend/lait/modules/exercise_gap_fill/evaluate.py`
- FOUND: `backend/lait/modules/exercise_gap_fill/feedback.py`
- FOUND: `backend/lait/modules/exercise_gap_fill/sentence_window.py`
- FOUND: `backend/lait/modules/exercise_proof/generate.py`
- FOUND: `backend/lait/modules/exercise_proof/evaluate.py`
- FOUND: `f24c005`
- FOUND: `78de06d`
- FOUND: `d08ed96`
- FOUND: `9ac0732`
- FOUND: `7f95e9b`
- FOUND: `eb61413`

---
*Phase: 01-mod-first-manual-learning-loop*
*Completed: 2026-10-01*
