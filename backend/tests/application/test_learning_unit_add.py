"""learning_unit.add stores an exact draft span and rejects overlap."""

from __future__ import annotations

from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'units.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def _lesson(repository, source: str):
    from lait.application.commands.lesson_create import LessonCreate, handle

    return handle(LessonCreate(source=source), repository)


def test_add_stores_exact_span_text_as_draft(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import COMMAND_NAME, LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units

    source = "ship the queue"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    start = source.index("the queue")
    end = start + len("the queue")

    created = handle(
        LearningUnitAdd(lesson_id=lesson.id, start=start, end=end),
        repository,
        repository,
    )

    assert COMMAND_NAME == "learning_unit.add"
    assert created.status == "draft"
    assert created.text == "the queue"
    assert created.text == source[created.start : created.end]
    assert created.start == start
    assert created.end == end
    assert created.lesson_id == lesson.id
    assert created.removed_at is None
    listed = list_units(lesson.id, repository)
    assert [unit.id for unit in listed] == [created.id]
    assert listed[0].text == source[start:end]


def test_missing_span_writes_no_row(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units
    from lait.domain.learning_unit import MissingSpanError

    source = "ship the queue"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    with pytest.raises(MissingSpanError):
        handle(LearningUnitAdd(lesson_id=lesson.id, start=None, end=None), repository, repository)
    with pytest.raises(MissingSpanError):
        handle(LearningUnitAdd(lesson_id=lesson.id, start=0, end=0), repository, repository)

    assert list_units(lesson.id, repository) == []


def test_out_of_range_span_writes_no_row(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units
    from lait.domain.learning_unit import SpanOutOfRangeError

    source = "ship the queue"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    with pytest.raises(SpanOutOfRangeError):
        handle(
            LearningUnitAdd(lesson_id=lesson.id, start=-1, end=4),
            repository,
            repository,
        )
    with pytest.raises(SpanOutOfRangeError):
        handle(
            LearningUnitAdd(lesson_id=lesson.id, start=0, end=len(source) + 1),
            repository,
            repository,
        )

    assert list_units(lesson.id, repository) == []


def test_overlap_of_rolling_out_keeps_existing_unit(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units
    from lait.domain.learning_unit import SpanOverlapError

    source = "I was responsible for rolling out the migration."
    existing_text = "responsible for rolling out"
    incoming_text = "rolling out"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    existing_start = source.index(existing_text)
    created = handle(
        LearningUnitAdd(
            lesson_id=lesson.id,
            start=existing_start,
            end=existing_start + len(existing_text),
        ),
        repository,
        repository,
    )
    incoming_start = source.index(incoming_text)

    with pytest.raises(SpanOverlapError):
        handle(
            LearningUnitAdd(
                lesson_id=lesson.id,
                start=incoming_start,
                end=incoming_start + len(incoming_text),
            ),
            repository,
            repository,
        )

    listed = list_units(lesson.id, repository)
    assert [unit.id for unit in listed] == [created.id]
    assert listed[0].text == existing_text
    assert listed[0].text == source[listed[0].start : listed[0].end]


def test_touching_edges_create_two_units(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units

    source = "responsible for rolling out"
    left = "responsible for "
    right = "rolling out"
    assert source.index(right) == len(left)
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    first = handle(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=len(left)),
        repository,
        repository,
    )
    second = handle(
        LearningUnitAdd(lesson_id=lesson.id, start=len(left), end=len(source)),
        repository,
        repository,
    )

    assert first.id != second.id
    assert first.text == left
    assert second.text == right
    assert {unit.id for unit in list_units(lesson.id, repository)} == {first.id, second.id}


def test_same_phrase_in_two_places_creates_two_units(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.application.queries.learning_unit_list import handle as list_units

    source = "rolling out the rolling out"
    phrase = "rolling out"
    first_start = source.index(phrase)
    second_start = source.index(phrase, first_start + len(phrase))
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    first = handle(
        LearningUnitAdd(
            lesson_id=lesson.id,
            start=first_start,
            end=first_start + len(phrase),
        ),
        repository,
        repository,
    )
    second = handle(
        LearningUnitAdd(
            lesson_id=lesson.id,
            start=second_start,
            end=second_start + len(phrase),
        ),
        repository,
        repository,
    )

    assert first.id != second.id
    assert first.text == second.text == phrase
    assert {unit.id for unit in list_units(lesson.id, repository)} == {first.id, second.id}


def test_offsets_are_unicode_code_points_not_utf16(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd, handle
    from lait.domain.learning_unit import SpanOutOfRangeError

    source = "👍out"
    assert len(source) == 4
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)

    created = handle(
        LearningUnitAdd(lesson_id=lesson.id, start=1, end=4),
        repository,
        repository,
    )
    assert created.text == "out"
    assert created.start == 1
    assert created.end == 4

    with pytest.raises(SpanOutOfRangeError):
        handle(
            LearningUnitAdd(lesson_id=lesson.id, start=2, end=5),
            repository,
            repository,
        )
