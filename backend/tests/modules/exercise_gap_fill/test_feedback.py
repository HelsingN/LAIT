"""Gap Fill feedback uses the D-18 templates and records used or missed chunks."""

from __future__ import annotations


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


def test_correct_explanation_matches_d18_and_records_used() -> None:
    from lait.domain.exercise import TypedAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate
    from lait.modules.exercise_gap_fill.feedback import explanation

    unit = "rolling out"
    submitted = "Rolling out"
    assert explanation(category="correct", submitted=submitted, unit=unit) == (
        'Correct. The expected answer is "rolling out".'
    )

    result = evaluate(_item(), TypedAnswer(submitted))
    assert result.category == "correct"
    assert result.explanation == 'Correct. The expected answer is "rolling out".'
    assert result.natural_alternative is None
    assert result.chunks_used == ("rolling out",)
    assert result.chunks_missed == ()
    assert result.submitted == submitted
    assert result.expected == unit


def test_incorrect_explanation_matches_d18_and_records_missed() -> None:
    from lait.domain.exercise import TypedAnswer
    from lait.modules.exercise_gap_fill.evaluate import evaluate
    from lait.modules.exercise_gap_fill.feedback import explanation

    submitted = "  ship it  "
    unit = "rolling out"
    assert explanation(category="incorrect", submitted=submitted, unit=unit) == (
        'Your answer: "  ship it  ".'
    )

    result = evaluate(_item(), TypedAnswer(submitted))
    assert result.category == "incorrect"
    assert result.explanation == 'Your answer: "  ship it  ".'
    assert "Expected" not in result.explanation
    assert result.natural_alternative is None
    assert result.chunks_used == ()
    assert result.chunks_missed == ("rolling out",)
    assert result.submitted == submitted
