"""learning_unit.accept moves a draft into the accepted pool."""

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


def test_accept_flips_draft_and_list_returns_both(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_accept import (
        COMMAND_NAME,
        LearningUnitAccept,
        handle,
    )
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.queries.learning_unit_list import QUERY_NAME, handle as list_units

    source = "alpha beta gamma"
    repository = _repository(tmp_path)
    lesson = _lesson(repository, source)
    draft = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=0, end=len("alpha")),
        repository,
        repository,
    )
    pending = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=source.index("gamma"), end=len(source)),
        repository,
        repository,
    )
    assert draft.status == "draft"
    assert pending.status == "draft"

    accepted = handle(
        LearningUnitAccept(lesson_id=lesson.id, unit_id=pending.id),
        repository,
        repository,
    )

    assert COMMAND_NAME == "learning_unit.accept"
    assert QUERY_NAME == "learning_unit.list"
    assert accepted.id == pending.id
    assert accepted.status == "accepted"
    assert accepted.text == "gamma"
    listed = list_units(lesson.id, repository)
    by_id = {unit.id: unit for unit in listed}
    assert set(by_id) == {draft.id, accepted.id}
    assert by_id[draft.id].status == "draft"
    assert by_id[accepted.id].status == "accepted"


def test_accept_unknown_unit_writes_nothing(tmp_path: Path) -> None:
    from lait.application.commands.learning_unit_accept import LearningUnitAccept, handle
    from lait.application.queries.learning_unit_list import handle as list_units
    from lait.domain.learning_unit import LearningUnitNotFoundError

    repository = _repository(tmp_path)
    lesson = _lesson(repository, "alpha beta")

    with pytest.raises(LearningUnitNotFoundError):
        handle(
            LearningUnitAccept(lesson_id=lesson.id, unit_id="missing-unit"),
            repository,
            repository,
        )
    assert list_units(lesson.id, repository) == []
