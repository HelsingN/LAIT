"""Gap Fill evaluate: drag identity, typed trim+casefold, two emitted categories."""

from __future__ import annotations

import typing


def _item():
    from lait.domain.exercise import ExerciseItem, PromptSegment

    return ExerciseItem(
        learning_unit_id="u1",
        exercise_type="gap-fill",
        start=0,
        end=11,
        target_text="rolling out",
        sentence="______",
        segments=(PromptSegment(kind="blank", text="______"),),
    )


def test_drag_is_correct_when_submitted_learning_unit_id_matches() -> None:
    from lait.domain.exercise import DragAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate

    result = evaluate(_item(), DragAnswer(learning_unit_id="u1", text="rolling out"))
    assert result.category == "correct"


def test_drag_is_incorrect_for_other_unit_id_even_when_text_matches() -> None:
    from lait.domain.exercise import DragAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate

    result = evaluate(_item(), DragAnswer(learning_unit_id="u2", text="rolling out"))
    assert result.category == "incorrect"
    assert result.submitted == "rolling out"
    assert result.expected == "rolling out"


def test_typed_match_strips_ends_and_ignores_case_only() -> None:
    from lait.domain.exercise import TypedAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate, typed_match

    assert typed_match("Rolling out", "rolling out") is True
    assert typed_match("  rolling out  ", "rolling out") is True
    assert typed_match("rolling  out", "rolling out") is False
    assert typed_match("rolling out.", "rolling out") is False
    assert typed_match("rolling out's", "rolling out") is False

    item = _item()
    assert evaluate(item, TypedAnswer("Rolling out")).category == "correct"
    assert evaluate(item, TypedAnswer("  rolling out  ")).category == "correct"
    assert evaluate(item, TypedAnswer("rolling  out")).category == "incorrect"
    assert evaluate(item, TypedAnswer("rolling out.")).category == "incorrect"
    assert evaluate(item, TypedAnswer("rolling out's")).category == "incorrect"


def test_gap_fill_emits_only_correct_or_incorrect() -> None:
    from lait.domain.exercise import RESULT_CATEGORIES, DragAnswer, ResultCategory, TypedAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate

    assert RESULT_CATEGORIES == (
        "correct",
        "acceptable",
        "partial",
        "incorrect",
        "uncertain",
    )
    assert typing.get_args(ResultCategory) == RESULT_CATEGORIES

    item = _item()
    categories = {
        evaluate(item, DragAnswer(learning_unit_id="u1", text="rolling out")).category,
        evaluate(item, DragAnswer(learning_unit_id="u2", text="rolling out")).category,
        evaluate(item, TypedAnswer("Rolling out")).category,
        evaluate(item, TypedAnswer("rolling  out")).category,
    }
    assert categories == {"correct", "incorrect"}
