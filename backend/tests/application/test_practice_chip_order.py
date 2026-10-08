"""Chip order is a per-item permutation. Grading still uses the unit id."""

from __future__ import annotations

from datetime import UTC, datetime


def test_permute_repeats_and_is_not_the_stored_span_order() -> None:
    from lait.application.queries.chip_order import permute_chip_ids

    ids = ("u1", "u2", "u3", "u4")
    first = permute_chip_ids(ids, session_id="session-a", item_id="unit-1")
    again = permute_chip_ids(ids, session_id="session-a", item_id="unit-1")

    assert first == again
    assert tuple(sorted(first)) == tuple(sorted(ids))
    assert first != ids


def test_session_and_item_each_change_the_order() -> None:
    from lait.application.queries.chip_order import permute_chip_ids

    ids = ("u1", "u2", "u3", "u4")
    session_a = permute_chip_ids(ids, session_id="session-a", item_id="unit-1")
    session_b = permute_chip_ids(ids, session_id="session-b", item_id="unit-1")
    other_item = permute_chip_ids(ids, session_id="session-a", item_id="unit-2")

    assert session_b != session_a
    assert other_item != session_a


def test_one_id_stays_and_two_ids_are_never_the_input_order() -> None:
    from lait.application.queries.chip_order import permute_chip_ids

    assert permute_chip_ids(("only",), session_id="session-a", item_id="unit-1") == ("only",)
    pair = ("u1", "u2")
    assert permute_chip_ids(pair, session_id="session-a", item_id="unit-1") != pair
    assert permute_chip_ids(pair, session_id="session-b", item_id="unit-2") != pair


def test_view_for_permutes_the_current_item_and_leaves_the_generation() -> None:
    from lait.application.queries.practice_get import view_for
    from lait.domain.exercise import PromptSegment
    from lait.domain.practice_session import (
        COMPLETED,
        DRAG,
        OPEN,
        ExerciseDefinition,
        ExerciseGeneration,
        PassItem,
        PracticeSession,
    )

    chips = ("u1", "u2", "u3", "u4")
    created_at = datetime(2026, 10, 2, tzinfo=UTC)
    definitions = tuple(
        ExerciseDefinition(
            id=f"def-{unit_id}",
            learning_unit_id=unit_id,
            exercise_type="gap-fill",
            module_package="official.exercise.gap-fill",
            position=index,
            start=index,
            end=index + 1,
            target_text=unit_id,
            sentence="______",
            segments=(PromptSegment(kind="blank", text="______"),),
        )
        for index, unit_id in enumerate(chips)
    )
    generation = ExerciseGeneration(
        id="generation-1",
        lesson_id="lesson-1",
        status=COMPLETED,
        accepted_unit_ids=chips,
        chip_unit_ids=chips,
        created_at=created_at,
        definitions=definitions,
    )

    def session(session_id: str) -> PracticeSession:
        return PracticeSession(
            id=session_id,
            lesson_id=generation.lesson_id,
            generation_id=generation.id,
            status=OPEN,
            cursor=0,
            items=(
                PassItem(
                    position=0,
                    mode=DRAG,
                    learning_unit_id="u1",
                    definition_id="def-u1",
                ),
            ),
        )

    stored = generation.chip_unit_ids
    view_a = view_for(session("session-a"), generation)
    view_b = view_for(session("session-b"), generation)

    assert generation.chip_unit_ids == stored == chips
    assert view_a.current is not None
    assert view_b.current is not None
    assert tuple(sorted(view_a.current.chip_unit_ids)) == chips
    assert view_a.current.chip_unit_ids != chips
    assert view_b.current.chip_unit_ids != view_a.current.chip_unit_ids


def test_drag_grade_follows_the_unit_id_when_the_chip_tuple_is_reversed() -> None:
    from lait.domain.exercise import DragAnswer, ExerciseItem, PromptSegment
    from lait.modules.exercise_gap_fill.evaluate import evaluate

    item = ExerciseItem(
        learning_unit_id="u1",
        exercise_type="gap-fill",
        start=0,
        end=3,
        target_text="u1",
        sentence="______",
        segments=(PromptSegment(kind="blank", text="______"),),
    )
    chips = ("u1", "u2", "u3", "u4")
    reversed_chips = tuple(reversed(chips))
    assert reversed_chips != chips

    matched = evaluate(item, DragAnswer(learning_unit_id=item.learning_unit_id, text="first chip"))
    other = evaluate(item, DragAnswer(learning_unit_id="u4", text="last chip"))

    assert matched.category == "correct"
    assert other.category == "incorrect"
    assert evaluate(item, DragAnswer(learning_unit_id=item.learning_unit_id, text="moved")).category == "correct"
