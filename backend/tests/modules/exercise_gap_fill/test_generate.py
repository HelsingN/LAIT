"""Gap Fill generate blanks only the target span inside its sentence window."""

from __future__ import annotations


def test_one_accepted_unit_blanks_only_the_target_span() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate

    source = "I was responsible for rolling out the migration."
    start = source.index("rolling out")
    end = start + len("rolling out")
    result = generate(
        source,
        [AcceptedUnit(learning_unit_id="u1", start=start, end=end, text="rolling out")],
    )

    assert len(result.items) == 1
    item = result.items[0]
    assert item.learning_unit_id == "u1"
    assert item.exercise_type == "gap-fill"
    assert item.target_text == "rolling out"
    assert item.start == start
    assert item.end == end
    assert item.sentence == "I was responsible for ______ the migration."
    assert "responsible for" in item.sentence
    assert "the migration." in item.sentence
    assert "rolling out" not in item.sentence
    assert [segment.kind for segment in item.segments] == ["text", "blank", "text"]
    assert item.segments[0].text == "I was responsible for "
    assert item.segments[1].text == "______"
    assert item.segments[2].text == " the migration."


def test_sentence_window_keeps_only_the_target_sentence() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate
    from lait.modules.exercise_gap_fill.sentence_window import sentence_window

    source = "Skip this. I was responsible for rolling out the migration. And this."
    start = source.index("rolling out")
    end = start + len("rolling out")
    window_start, window_end = sentence_window(source, start, end)
    assert source[window_start:window_end] == " I was responsible for rolling out the migration."

    result = generate(
        source,
        [AcceptedUnit(learning_unit_id="u1", start=start, end=end, text="rolling out")],
    )
    item = result.items[0]
    assert item.sentence == " I was responsible for ______ the migration."
    assert "Skip this" not in item.sentence
    assert "And this" not in item.sentence


def test_sentence_window_uses_start_and_end_when_no_terminator() -> None:
    from lait.modules.exercise_gap_fill.sentence_window import sentence_window

    source = "rolling out the migration"
    start = source.index("rolling out")
    end = start + len("rolling out")
    window_start, window_end = sentence_window(source, start, end)
    assert source[window_start:window_end] == source


def test_sentence_window_honors_exclamation_and_question_marks() -> None:
    from lait.modules.exercise_gap_fill.sentence_window import sentence_window

    source = "Done! Keep rolling out? Later."
    start = source.index("rolling out")
    end = start + len("rolling out")
    window_start, window_end = sentence_window(source, start, end)
    assert source[window_start:window_end] == " Keep rolling out?"


def test_items_order_by_span_start_then_learning_unit_id() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate

    source = "alpha beta gamma."
    later = AcceptedUnit(
        learning_unit_id="u-later",
        start=source.index("gamma"),
        end=source.index("gamma") + len("gamma"),
        text="gamma",
    )
    earlier = AcceptedUnit(
        learning_unit_id="u-earlier",
        start=source.index("alpha"),
        end=source.index("alpha") + len("alpha"),
        text="alpha",
    )
    result = generate(source, [later, earlier])
    assert [item.learning_unit_id for item in result.items] == ["u-earlier", "u-later"]


def test_equal_span_start_orders_by_learning_unit_id() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate

    source = "alpha beta."
    result = generate(
        source,
        [
            AcceptedUnit(learning_unit_id="u-b", start=0, end=5, text="alpha"),
            AcceptedUnit(learning_unit_id="u-a", start=0, end=1, text="a"),
        ],
    )
    assert [item.learning_unit_id for item in result.items] == ["u-a", "u-b"]


def test_two_units_in_one_sentence_blank_only_their_own_span() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate

    source = "I was responsible for rolling out the migration."
    responsible_start = source.index("responsible for")
    rolling_start = source.index("rolling out")
    responsible = AcceptedUnit(
        learning_unit_id="responsible",
        start=responsible_start,
        end=responsible_start + len("responsible for"),
        text="responsible for",
    )
    rolling = AcceptedUnit(
        learning_unit_id="rolling",
        start=rolling_start,
        end=rolling_start + len("rolling out"),
        text="rolling out",
    )
    result = generate(source, [rolling, responsible])
    by_id = {item.learning_unit_id: item for item in result.items}

    assert by_id["responsible"].sentence == "I was ______ rolling out the migration."
    assert "rolling out" in by_id["responsible"].sentence
    assert "responsible for" not in by_id["responsible"].sentence
    assert by_id["rolling"].sentence == "I was responsible for ______ the migration."
    assert "responsible for" in by_id["rolling"].sentence
    assert "rolling out" not in by_id["rolling"].sentence


def test_generate_exposes_chip_candidate_unit_ids() -> None:
    from lait.domain.exercise import AcceptedUnit
    from lait.modules.exercise_gap_fill.generate import generate

    source = "I was responsible for rolling out the migration."
    responsible_start = source.index("responsible for")
    rolling_start = source.index("rolling out")
    result = generate(
        source,
        [
            AcceptedUnit(
                learning_unit_id="rolling",
                start=rolling_start,
                end=rolling_start + len("rolling out"),
                text="rolling out",
            ),
            AcceptedUnit(
                learning_unit_id="responsible",
                start=responsible_start,
                end=responsible_start + len("responsible for"),
                text="responsible for",
            ),
        ],
    )
    assert result.chip_unit_ids == ("responsible", "rolling")
