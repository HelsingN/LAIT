"""practice.start freezes the accepted set and serves one current item."""

from __future__ import annotations

from pathlib import Path

import pytest


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'practice.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def _registry():
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    return validate_catalog(load_bundled_catalog())


def _lesson(repository, source: str):
    from lait.application.commands.lesson_create import LessonCreate, handle

    return handle(LessonCreate(source=source), repository)


def _add(repository, lesson_id: str, source: str, text: str):
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit

    start = source.index(text)
    return add_unit(
        LearningUnitAdd(lesson_id=lesson_id, start=start, end=start + len(text)),
        repository,
        repository,
    )


def _accept_unit(repository, lesson_id: str, unit_id: str):
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit

    return accept_unit(
        LearningUnitAccept(lesson_id=lesson_id, unit_id=unit_id),
        repository,
        repository,
    )


def _generate(repository, lesson_id: str):
    from lait.application.commands.exercise_generate import ExerciseGenerate, handle

    return handle(ExerciseGenerate(lesson_id=lesson_id), repository, repository, _registry())


def test_start_freezes_add_remove_and_accept(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.learning_unit_remove import LearningUnitRemove
    from lait.application.commands.learning_unit_remove import handle as remove_unit
    from lait.application.commands.practice_start import COMMAND_NAME, PracticeStart, handle
    from lait.application.queries.learning_unit_list import handle as list_units
    from lait.domain.learning_unit import UnitSetFrozenError

    source = "alpha beta"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    accepted = _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    draft = _add(repository, lesson.id, source, "beta")
    _generate(repository, lesson.id)

    session = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    assert COMMAND_NAME == "practice.start"
    assert session.open is True
    before = [(unit.id, unit.status) for unit in list_units(lesson.id, repository)]
    with pytest.raises(UnitSetFrozenError):
        add_unit(
            LearningUnitAdd(lesson_id=lesson.id, start=0, end=len("alpha")),
            repository,
            repository,
        )
    with pytest.raises(UnitSetFrozenError):
        remove_unit(
            LearningUnitRemove(lesson_id=lesson.id, unit_id=accepted.id),
            repository,
            repository,
        )
    with pytest.raises(UnitSetFrozenError):
        accept_unit(
            LearningUnitAccept(lesson_id=lesson.id, unit_id=draft.id),
            repository,
            repository,
        )
    after = [(unit.id, unit.status) for unit in list_units(lesson.id, repository)]
    assert after == before
    assert repository.has_open_practice_session(lesson.id) is True


def test_start_rejects_stale_generation_after_accept_or_remove(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_remove import LearningUnitRemove
    from lait.application.commands.learning_unit_remove import handle as remove_unit
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.domain.practice_session import StaleGenerationError

    source = "alpha beta gamma"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "gamma").id)

    with pytest.raises(StaleGenerationError):
        handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    other = "left right"
    other_lesson = _lesson(repository, other)
    _accept_unit(repository, other_lesson.id, _add(repository, other_lesson.id, other, "left").id)
    right = _accept_unit(
        repository, other_lesson.id, _add(repository, other_lesson.id, other, "right").id
    )
    _generate(repository, other_lesson.id)
    remove_unit(
        LearningUnitRemove(lesson_id=other_lesson.id, unit_id=right.id),
        repository,
        repository,
    )
    with pytest.raises(StaleGenerationError):
        handle(PracticeStart(lesson_id=other_lesson.id), repository, repository, _registry())


def test_draft_only_add_does_not_invalidate_generation(tmp_path: Path) -> None:
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.application.queries.practice_get import QUERY_NAME
    from lait.application.queries.practice_get import handle as current_item

    source = "alpha beta"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    accepted = _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)
    _add(repository, lesson.id, source, "beta")

    session = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    view = current_item(session.session_id, repository)

    assert QUERY_NAME == "practice.get"
    assert view.open is True
    assert view.current is not None
    assert view.current.mode == "typed"
    assert view.current.learning_unit_id == accepted.id
    assert view.current.position == 0


def test_practice_get_returns_one_current_typed_item_for_one_unit(tmp_path: Path) -> None:
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.application.queries.practice_get import handle as current_item

    source = "I was responsible for rolling out the migration."
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    added = _add(repository, lesson.id, source, "rolling out")
    unit = _accept_unit(repository, lesson.id, added.id)
    _generate(repository, lesson.id)

    session = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    view = current_item(session.session_id, repository)

    assert view.session_id == session.session_id
    assert view.current is not None
    assert view.current.mode == "typed"
    assert view.current.learning_unit_id == unit.id
    assert view.current.target_text == "rolling out"
    assert "______" in view.current.sentence
    assert not hasattr(view, "items")
    assert repository.has_open_practice_session(lesson.id) is True


def test_two_unit_lesson_yields_drag_then_typed_in_span_order(tmp_path: Path) -> None:
    from lait.application.commands.exercise_submit_attempt import SubmitAttempt
    from lait.application.commands.exercise_submit_attempt import handle as submit
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.application.queries.practice_get import handle as current_item

    source = "zzzz middle aaaa"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    later = _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "aaaa").id)
    earlier = _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "zzzz").id)
    assert source.index("zzzz") < source.index("aaaa")
    outcome = _generate(repository, lesson.id)
    assert outcome.definition_count == 2

    session = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    modes: list[str] = []
    unit_ids: list[str] = []
    view = current_item(session.session_id, repository)
    while view.current is not None:
        assert not hasattr(view, "items")
        assert view.current.mode in {"drag", "typed"}
        modes.append(view.current.mode)
        unit_ids.append(view.current.learning_unit_id)
        if view.current.mode == "drag":
            submit(
                SubmitAttempt(
                    session_id=session.session_id,
                    kind="drag",
                    text=view.current.target_text,
                    submitted_unit_id=view.current.learning_unit_id,
                ),
                repository,
                _registry(),
            )
        else:
            submit(
                SubmitAttempt(
                    session_id=session.session_id,
                    kind="typed",
                    text=view.current.target_text,
                ),
                repository,
                _registry(),
            )
        view = current_item(session.session_id, repository)

    assert modes == ["drag", "drag", "typed", "typed"]
    assert unit_ids == [earlier.id, later.id, earlier.id, later.id]
    assert view.open is True
    assert view.current is None
    assert repository.has_open_practice_session(lesson.id) is True
