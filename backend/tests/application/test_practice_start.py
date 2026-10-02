"""practice.start freezes the accepted set and serves one current item."""

from __future__ import annotations

import json
import sqlite3
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


def _database(tmp_path: Path) -> tuple[object, str]:
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'practice.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url), database_url


def _open_session_ids(database_url: str) -> list[str]:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        rows = connection.execute(
            "select id from practice_sessions where status = 'open' order by id"
        ).fetchall()
    finally:
        connection.close()
    return [session_id for (session_id,) in rows]


def _rewrite_open_generation_snapshot(database_url: str, unit_ids: list[str]) -> None:
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        connection.execute(
            """
            update exercise_generations
            set accepted_unit_ids = ?
            where id = (
                select generation_id from practice_sessions where status = 'open'
            )
            """,
            (json.dumps(unit_ids),),
        )
        connection.commit()
    finally:
        connection.close()


def test_second_start_returns_the_same_open_session(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.domain.learning_unit import UnitSetFrozenError

    source = "alpha beta"
    repository, database_url = _database(tmp_path)
    lesson = _lesson(repository, source)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)

    first = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    second = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    assert second.session_id == first.session_id
    assert _open_session_ids(database_url) == [first.session_id]
    assert repository.has_open_practice_session(lesson.id) is True
    with pytest.raises(UnitSetFrozenError):
        add_unit(
            LearningUnitAdd(lesson_id=lesson.id, start=0, end=len("alpha")),
            repository,
            repository,
        )


def test_generate_again_keeps_the_open_session_for_the_next_start(tmp_path: Path) -> None:
    from lait.application.commands.practice_start import PracticeStart, handle

    source = "alpha beta"
    repository, database_url = _database(tmp_path)
    lesson = _lesson(repository, source)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)
    first = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    _generate(repository, lesson.id)
    second = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    assert second.session_id == first.session_id
    assert _open_session_ids(database_url) == [first.session_id]
    assert repository.has_open_practice_session(lesson.id) is True


def test_open_session_snapshot_mismatch_stays_open_and_frozen(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.practice_start import PracticeStart, handle
    from lait.domain.learning_unit import UnitSetFrozenError
    from lait.domain.practice_session import StaleGenerationError

    source = "alpha beta"
    repository, database_url = _database(tmp_path)
    lesson = _lesson(repository, source)
    accepted = _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    draft = _add(repository, lesson.id, source, "beta")
    _generate(repository, lesson.id)
    first = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    _rewrite_open_generation_snapshot(database_url, ["not-the-accepted-unit"])

    with pytest.raises(StaleGenerationError):
        handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())

    assert _open_session_ids(database_url) == [first.session_id]
    with pytest.raises(UnitSetFrozenError):
        accept_unit(
            LearningUnitAccept(lesson_id=lesson.id, unit_id=draft.id),
            repository,
            repository,
        )
    assert repository.has_open_practice_session(lesson.id) is True
    assert accepted.id != draft.id


def test_second_open_row_for_one_lesson_is_rejected(tmp_path: Path) -> None:
    from sqlalchemy import create_engine
    from sqlalchemy.exc import IntegrityError
    from sqlalchemy.orm import sessionmaker

    from lait.adapters.persistence.models import PracticeSessionRow
    from lait.application.commands.practice_start import PracticeStart, handle

    source = "alpha beta"
    repository, database_url = _database(tmp_path)
    lesson = _lesson(repository, source)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)
    first = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        generation_id = connection.execute(
            "select generation_id from practice_sessions where id = ?",
            (first.session_id,),
        ).fetchone()
    finally:
        connection.close()
    assert generation_id is not None

    engine = create_engine(database_url)
    factory = sessionmaker(bind=engine)
    with factory() as session:
        session.add(
            PracticeSessionRow(
                id="second-open",
                lesson_id=lesson.id,
                generation_id=generation_id[0],
                status="open",
                cursor=0,
                created_at="2026-10-02T00:00:00+00:00",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
    engine.dispose()

    connection = sqlite3.connect(database_url.removeprefix("sqlite:///"))
    try:
        index_row = connection.execute(
            "select sql from sqlite_master where type = 'index' and name = ?",
            ("uq_practice_sessions_one_open_per_lesson",),
        ).fetchone()
    finally:
        connection.close()
    assert index_row is not None
    assert "uq_practice_sessions_one_open_per_lesson" in index_row[0]
    assert _open_session_ids(database_url) == [first.session_id]


def test_unique_violation_returns_the_winning_open_session(tmp_path: Path) -> None:
    from sqlalchemy import create_engine, event

    from lait.adapters.persistence.models import PracticeSessionRow
    from lait.application.commands.practice_start import PracticeStart, handle

    source = "alpha beta"
    repository, database_url = _database(tmp_path)
    lesson = _lesson(repository, source)
    _accept_unit(repository, lesson.id, _add(repository, lesson.id, source, "alpha").id)
    _generate(repository, lesson.id)
    winner_id = "winner-open"
    fired = {"done": False}

    def before_insert(_mapper, _connection, target) -> None:
        if fired["done"] or target.id == winner_id:
            return
        fired["done"] = True
        other = create_engine(database_url)
        with other.begin() as connection:
            connection.execute(
                PracticeSessionRow.__table__.insert(),
                {
                    "id": winner_id,
                    "lesson_id": target.lesson_id,
                    "generation_id": target.generation_id,
                    "status": "open",
                    "cursor": 0,
                    "created_at": target.created_at,
                },
            )
        other.dispose()

    event.listen(PracticeSessionRow, "before_insert", before_insert)
    try:
        view = handle(PracticeStart(lesson_id=lesson.id), repository, repository, _registry())
    finally:
        event.remove(PracticeSessionRow, "before_insert", before_insert)

    assert fired["done"] is True
    assert view.session_id == winner_id
    assert view.open is True
    assert _open_session_ids(database_url) == [winner_id]
