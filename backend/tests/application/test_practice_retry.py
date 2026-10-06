"""A miss stays on the item. A later match is corrected, not a first-try correct."""

from __future__ import annotations

from pathlib import Path


def _repository(tmp_path: Path):
    from lait.adapters.persistence.database import migrate, open_repository

    database_url = f"sqlite:///{(tmp_path / 'retry.db').as_posix()}"
    migrate(database_url)
    return open_repository(database_url)


def _registry():
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    return validate_catalog(load_bundled_catalog())


def _session(tmp_path: Path, phrases: tuple[str, ...] = ("rolling out",)):
    from lait.application.commands.exercise_generate import ExerciseGenerate
    from lait.application.commands.exercise_generate import handle as generate
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.lesson_create import LessonCreate
    from lait.application.commands.lesson_create import handle as create_lesson
    from lait.application.commands.practice_start import PracticeStart
    from lait.application.commands.practice_start import handle as start

    source = "I was responsible for rolling out the migration."
    repository = _repository(tmp_path)
    lesson = create_lesson(LessonCreate(source=source), repository)
    registry = _registry()
    units = []
    for phrase in phrases:
        start_at = source.index(phrase)
        created = add_unit(
            LearningUnitAdd(lesson_id=lesson.id, start=start_at, end=start_at + len(phrase)),
            repository,
            repository,
        )
        units.append(
            accept_unit(
                LearningUnitAccept(lesson_id=lesson.id, unit_id=created.id),
                repository,
                repository,
            )
        )
    generate(ExerciseGenerate(lesson_id=lesson.id), repository, repository, registry)
    session = start(PracticeStart(lesson_id=lesson.id), repository, repository, registry)
    return repository, lesson, units, session, registry


def _submit(
    repository,
    registry,
    session_id: str,
    kind: str,
    text: str,
    submitted_unit_id: str | None = None,
    target_learning_unit_id: str | None = None,
):
    from lait.application.commands.exercise_submit_attempt import SubmitAttempt
    from lait.application.commands.exercise_submit_attempt import handle as submit

    return submit(
        SubmitAttempt(
            session_id=session_id,
            kind=kind,
            text=text,
            submitted_unit_id=submitted_unit_id,
            target_learning_unit_id=target_learning_unit_id,
        ),
        repository,
        registry,
    )


def test_incorrect_stays_and_a_later_match_is_corrected(tmp_path: Path) -> None:
    from lait.application.commands.practice_advance import PracticeAdvance
    from lait.application.commands.practice_advance import handle as advance
    from lait.application.commands.practice_finish import PracticeFinish
    from lait.application.commands.practice_finish import handle as finish
    from lait.application.queries.attempt_list_for_lesson import handle as list_attempts
    from lait.domain.practice_session import NoCurrentItemError

    repository, lesson, _units, session, registry = _session(tmp_path)
    first = _submit(repository, registry, session.session_id, "typed", "nope")
    assert first.category == "incorrect"
    assert first.cursor == 0
    assert "Expected" not in first.explanation

    second = _submit(repository, registry, session.session_id, "typed", "nope again")
    assert second.category == "incorrect"
    assert second.cursor == 0
    assert second.attempt_id != first.attempt_id

    matched = _submit(repository, registry, session.session_id, "typed", "Rolling out")
    assert matched.category == "corrected"
    assert matched.cursor == 1

    keys = repository.list_attempt_keys_for_session(session.session_id)
    assert [key[3] for key in keys] == ["incorrect", "incorrect", "corrected"]
    assert keys[0][0] == first.attempt_id

    empty = tmp_path / "empty"
    empty.mkdir()
    with_no_attempt = _session(empty)
    try:
        advance(
            PracticeAdvance(session_id=with_no_attempt[3].session_id, position=0),
            with_no_attempt[0],
        )
        raised = False
    except NoCurrentItemError:
        raised = True
    assert raised is True

    advanced = tmp_path / "advanced"
    advanced.mkdir()
    repository, lesson, units, session, registry = _session(advanced)
    _submit(repository, registry, session.session_id, "typed", "nope")
    moved = advance(PracticeAdvance(session_id=session.session_id, position=0), repository)
    again = advance(PracticeAdvance(session_id=session.session_id, position=0), repository)
    assert moved.cursor == 1
    assert again.cursor == 1
    assert len(repository.list_attempt_keys_for_session(session.session_id)) == 1

    finish(PracticeFinish(session_id=session.session_id), repository)
    listed = list_attempts(lesson.id, repository)
    assert [row.category for row in listed.attempts] == ["incorrect"]
    assert listed.attempts[0].pass_item_count == 1


def test_repeat_round_keeps_pair_identity_and_opening_size(tmp_path: Path) -> None:
    from lait.adapters.persistence.database import open_repository
    from lait.application.commands.practice_advance import PracticeAdvance
    from lait.application.commands.practice_advance import handle as advance
    from lait.application.commands.practice_finish import PracticeFinish
    from lait.application.commands.practice_finish import handle as finish
    from lait.application.queries.attempt_list_for_lesson import handle as list_attempts

    repository, lesson, units, session, registry = _session(
        tmp_path, ("rolling out", "the migration")
    )
    rolling, migration = units
    session_id = session.session_id
    correct = _submit(repository, registry, session_id, "drag", "rolling out", rolling.id)
    assert correct.category == "correct"
    missed_drag = _submit(repository, registry, session_id, "drag", "rolling out", rolling.id)
    assert missed_drag.category == "incorrect"
    assert missed_drag.cursor == 1
    advance(PracticeAdvance(session_id=session_id, position=1), repository)
    missed_typed = _submit(repository, registry, session_id, "typed", "nope")
    assert missed_typed.category == "incorrect"
    advance(PracticeAdvance(session_id=session_id, position=2), repository)
    typed_ok = _submit(repository, registry, session_id, "typed", "The migration")
    assert typed_ok.category == "correct"

    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert practice.cursor == 4
    assert [(item.mode, item.learning_unit_id) for item in practice.items[4:]] == [
        ("drag", migration.id),
        ("typed", rolling.id),
    ]
    assert practice.items[4].position == 4

    corrected = _submit(
        repository,
        registry,
        session_id,
        "drag",
        "the migration",
        migration.id,
        target_learning_unit_id=migration.id,
    )
    assert corrected.category == "corrected"
    assert corrected.cursor == 5
    keys = repository.list_attempt_keys_for_session(session_id)
    assert keys[1][3] == "incorrect"
    assert keys[1][0] == missed_drag.attempt_id

    advance(PracticeAdvance(session_id=session_id, position=5), repository)
    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert [(item.mode, item.learning_unit_id) for item in practice.items[6:]] == [
        ("typed", rolling.id)
    ]
    assert practice.cursor == 6
    before = len(practice.items)
    finish(PracticeFinish(session_id=session_id), repository)
    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert len(practice.items) == before

    fresh = open_repository(f"sqlite:///{(tmp_path / 'retry.db').as_posix()}")
    listed = list_attempts(lesson.id, fresh)
    assert {row.pass_item_count for row in listed.attempts} == {4}
    earliest: dict[tuple[str, str], str] = {}
    for row in listed.attempts:
        earliest.setdefault((row.mode, row.unit_text), row.category)
    assert earliest == {
        ("drag", "rolling out"): "correct",
        ("drag", "the migration"): "incorrect",
        ("typed", "rolling out"): "incorrect",
        ("typed", "the migration"): "correct",
    }
    assert "corrected" in [row.category for row in listed.attempts]


def test_eight_item_pass_stays_eight_after_two_copies(tmp_path: Path) -> None:
    from lait.adapters.persistence.database import open_repository
    from lait.application.commands.practice_advance import PracticeAdvance
    from lait.application.commands.practice_advance import handle as advance
    from lait.application.queries.attempt_list_for_lesson import handle as list_attempts

    phrases = ("I was", "responsible", "rolling out", "the migration")
    repository, lesson, units, session, registry = _session(tmp_path, phrases)
    session_id = session.session_id
    for unit in units:
        stored = _submit(repository, registry, session_id, "drag", unit.text, unit.id)
        assert stored.category == "correct"
    for index, unit in enumerate(units):
        if index < 2:
            stored = _submit(repository, registry, session_id, "typed", unit.text)
            assert stored.category == "correct"
            continue
        stored = _submit(repository, registry, session_id, "typed", "nope")
        assert stored.category == "incorrect"
        advance(PracticeAdvance(session_id=session_id, position=4 + index), repository)

    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert len(practice.items) == 10
    fresh = open_repository(f"sqlite:///{(tmp_path / 'retry.db').as_posix()}")
    listed = list_attempts(lesson.id, fresh)
    assert {row.pass_item_count for row in listed.attempts} == {8}
    earliest: dict[tuple[str, str], str] = {}
    for row in listed.attempts:
        earliest.setdefault((row.mode, row.unit_text), row.category)
    assert sum(category == "correct" for category in earliest.values()) == 6


def test_named_target_on_a_repeat_copy_advances_once(tmp_path: Path) -> None:
    from lait.application.commands.practice_advance import PracticeAdvance
    from lait.application.commands.practice_advance import handle as advance
    from lait.application.queries.practice_get import handle as get_practice

    repository, _lesson, units, session, registry = _session(
        tmp_path, ("rolling out", "the migration")
    )
    rolling, migration = units
    session_id = session.session_id
    missed_drag = _submit(
        repository,
        registry,
        session_id,
        "drag",
        "the migration",
        migration.id,
        target_learning_unit_id=rolling.id,
    )
    assert missed_drag.category == "incorrect"
    assert missed_drag.cursor == 0
    advance(PracticeAdvance(session_id=session_id, position=0), repository)
    _submit(
        repository,
        registry,
        session_id,
        "drag",
        "the migration",
        migration.id,
        target_learning_unit_id=migration.id,
    )
    missed_typed = _submit(
        repository,
        registry,
        session_id,
        "typed",
        "nope",
        target_learning_unit_id=rolling.id,
    )
    assert missed_typed.category == "incorrect"
    advance(PracticeAdvance(session_id=session_id, position=2), repository)
    _submit(
        repository,
        registry,
        session_id,
        "typed",
        "The migration",
        target_learning_unit_id=migration.id,
    )

    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert practice.cursor == 4
    assert [(item.mode, item.learning_unit_id) for item in practice.items[4:]] == [
        ("drag", rolling.id),
        ("typed", rolling.id),
    ]

    choice = _submit(
        repository,
        registry,
        session_id,
        "drag",
        "rolling out",
        rolling.id,
        target_learning_unit_id=rolling.id,
    )
    assert choice.category == "corrected"
    assert choice.cursor == 5
    view = get_practice(session_id, repository)
    assert view.current is not None
    assert view.current.position == 5
    assert view.current.mode == "typed"
    assert view.current.learning_unit_id == rolling.id

    typed = _submit(
        repository,
        registry,
        session_id,
        "typed",
        "Rolling out",
        target_learning_unit_id=rolling.id,
    )
    assert typed.category == "corrected"
    assert typed.cursor == 6
    assert get_practice(session_id, repository).current is None

    again = _submit(
        repository,
        registry,
        session_id,
        "typed",
        "Rolling out",
        target_learning_unit_id=rolling.id,
    )
    assert again.cursor == 6
    practice = repository.get_practice_session(session_id)
    assert practice is not None
    assert len(practice.items) == 6
