"""SQLite lesson, learning-unit, and practice repositories."""

from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from lait.adapters.persistence.lesson_repository import SqlAlchemyLessonRepository
from lait.adapters.persistence.models import (
    AttemptRow,
    ExerciseDefinitionRow,
    ExerciseGenerationRow,
    LearningUnitRow,
    PracticePassItemRow,
    PracticeSessionRow,
)
from lait.domain.exercise import PromptSegment
from lait.domain.learning_unit import LearningUnit, LearningUnitNotFoundError
from lait.domain.lesson import Lesson
from lait.domain.practice_session import (
    COMPLETED,
    OPEN,
    Attempt,
    AttemptRecord,
    ExerciseDefinition,
    ExerciseGeneration,
    NoCurrentItemError,
    PassItem,
    PracticeSession,
    PracticeSessionNotFoundError,
)


def _opening_pass_size(definition_count: int) -> int:
    if definition_count > 1:
        return definition_count * 2
    return definition_count


def _listed_pass_size(definition_count: int, item_count: int) -> int:
    opening = _opening_pass_size(definition_count)
    if opening > 0:
        return opening
    return item_count


def _still_uncorrected(categories: list[str]) -> bool:
    if "incorrect" not in categories:
        return False
    return "correct" not in categories and "corrected" not in categories


def _to_unit(row: LearningUnitRow) -> LearningUnit:
    return LearningUnit(
        id=row.id,
        lesson_id=row.lesson_id,
        start=row.span_start,
        end=row.span_end,
        text=row.text,
        status=row.status,
        created_at=datetime.fromisoformat(row.created_at),
        removed_at=None if row.removed_at is None else datetime.fromisoformat(row.removed_at),
    )


def _segments(raw: str) -> tuple[PromptSegment, ...]:
    payload = json.loads(raw)
    return tuple(PromptSegment(kind=item["kind"], text=item["text"]) for item in payload)


def _dump_segments(segments: tuple[PromptSegment, ...]) -> str:
    return json.dumps([{"kind": segment.kind, "text": segment.text} for segment in segments])


def _ids(raw: str) -> tuple[str, ...]:
    return tuple(json.loads(raw))


def _saved_chunks(raw: str) -> tuple[str, ...]:
    payload = json.loads(raw)
    if not isinstance(payload, list) or any(not isinstance(chunk, str) for chunk in payload):
        raise ValueError("Saved feedback chunks must be a JSON array of strings")
    return tuple(payload)


def _dump_ids(values: tuple[str, ...]) -> str:
    return json.dumps(list(values))


def _to_definition(row: ExerciseDefinitionRow) -> ExerciseDefinition:
    return ExerciseDefinition(
        id=row.id,
        learning_unit_id=row.learning_unit_id,
        exercise_type=row.exercise_type,
        module_package=row.module_package,
        position=row.position,
        start=row.span_start,
        end=row.span_end,
        target_text=row.target_text,
        sentence=row.sentence,
        segments=_segments(row.segments),
    )


def _to_generation(
    row: ExerciseGenerationRow,
    definitions: list[ExerciseDefinitionRow],
) -> ExerciseGeneration:
    ordered = sorted(definitions, key=lambda item: item.position)
    return ExerciseGeneration(
        id=row.id,
        lesson_id=row.lesson_id,
        status=row.status,
        accepted_unit_ids=_ids(row.accepted_unit_ids),
        chip_unit_ids=_ids(row.chip_unit_ids),
        created_at=datetime.fromisoformat(row.created_at),
        definitions=tuple(_to_definition(item) for item in ordered),
    )


def _to_session(row: PracticeSessionRow, items: list[PracticePassItemRow]) -> PracticeSession:
    ordered = sorted(items, key=lambda item: item.position)
    return PracticeSession(
        id=row.id,
        lesson_id=row.lesson_id,
        generation_id=row.generation_id,
        status=row.status,
        cursor=row.cursor,
        items=tuple(
            PassItem(
                position=item.position,
                mode=item.mode,
                learning_unit_id=item.learning_unit_id,
                definition_id=item.definition_id,
            )
            for item in ordered
        ),
    )


class SqlAlchemyPracticeRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def has_open_practice_session(self, lesson_id: str) -> bool:
        statement = (
            select(PracticeSessionRow.id)
            .where(
                PracticeSessionRow.lesson_id == lesson_id,
                PracticeSessionRow.status == OPEN,
            )
            .limit(1)
        )
        with self._session_factory() as session:
            return session.scalar(statement) is not None

    def save_generation(self, generation: ExerciseGeneration) -> None:
        row = ExerciseGenerationRow(
            id=generation.id,
            lesson_id=generation.lesson_id,
            status=generation.status,
            accepted_unit_ids=_dump_ids(generation.accepted_unit_ids),
            chip_unit_ids=_dump_ids(generation.chip_unit_ids),
            created_at=generation.created_at.isoformat(),
        )
        definition_rows = [
            ExerciseDefinitionRow(
                id=definition.id,
                generation_id=generation.id,
                position=definition.position,
                learning_unit_id=definition.learning_unit_id,
                exercise_type=definition.exercise_type,
                module_package=definition.module_package,
                span_start=definition.start,
                span_end=definition.end,
                target_text=definition.target_text,
                sentence=definition.sentence,
                segments=_dump_segments(definition.segments),
            )
            for definition in generation.definitions
        ]
        with self._session_factory() as session:
            session.add(row)
            session.flush()
            session.add_all(definition_rows)
            session.commit()

    def latest_completed_generation(self, lesson_id: str) -> ExerciseGeneration | None:
        statement = (
            select(ExerciseGenerationRow)
            .where(
                ExerciseGenerationRow.lesson_id == lesson_id,
                ExerciseGenerationRow.status == COMPLETED,
            )
            .order_by(ExerciseGenerationRow.created_at.desc(), ExerciseGenerationRow.id.desc())
        )
        with self._session_factory() as session:
            row = session.scalars(statement).first()
            if row is None:
                return None
            return self._generation_in_session(session, row)

    def get_generation(self, generation_id: str) -> ExerciseGeneration | None:
        with self._session_factory() as session:
            row = session.get(ExerciseGenerationRow, generation_id)
            if row is None:
                return None
            return self._generation_in_session(session, row)

    def get_open_practice_session(self, lesson_id: str) -> PracticeSession | None:
        with self._session_factory() as session:
            row = session.scalars(
                select(PracticeSessionRow).where(
                    PracticeSessionRow.lesson_id == lesson_id,
                    PracticeSessionRow.status == OPEN,
                )
            ).first()
            if row is None:
                return None
            return self._load_practice_session(session, row)

    def insert_open_practice_session(
        self, practice: PracticeSession, created_at: datetime
    ) -> PracticeSession:
        row = PracticeSessionRow(
            id=practice.id,
            lesson_id=practice.lesson_id,
            generation_id=practice.generation_id,
            status=practice.status,
            cursor=practice.cursor,
            created_at=created_at.isoformat(),
        )
        item_rows = [
            PracticePassItemRow(
                id=f"{practice.id}:{item.position}",
                session_id=practice.id,
                position=item.position,
                mode=item.mode,
                learning_unit_id=item.learning_unit_id,
                definition_id=item.definition_id,
            )
            for item in practice.items
        ]
        with self._session_factory() as session:
            try:
                existing = session.scalars(
                    select(PracticeSessionRow).where(
                        PracticeSessionRow.lesson_id == practice.lesson_id,
                        PracticeSessionRow.status == OPEN,
                    )
                ).first()
                if existing is not None:
                    return self._load_practice_session(session, existing)
                session.add(row)
                session.flush()
                session.add_all(item_rows)
                session.commit()
                return practice
            except IntegrityError:
                session.rollback()
                winner = session.scalars(
                    select(PracticeSessionRow).where(
                        PracticeSessionRow.lesson_id == practice.lesson_id,
                        PracticeSessionRow.status == OPEN,
                    )
                ).first()
                if winner is None:
                    raise
                return self._load_practice_session(session, winner)

    def save_practice_session(self, practice: PracticeSession, created_at: datetime) -> None:
        row = PracticeSessionRow(
            id=practice.id,
            lesson_id=practice.lesson_id,
            generation_id=practice.generation_id,
            status=practice.status,
            cursor=practice.cursor,
            created_at=created_at.isoformat(),
        )
        item_rows = [
            PracticePassItemRow(
                id=f"{practice.id}:{item.position}",
                session_id=practice.id,
                position=item.position,
                mode=item.mode,
                learning_unit_id=item.learning_unit_id,
                definition_id=item.definition_id,
            )
            for item in practice.items
        ]
        with self._session_factory() as session:
            session.add(row)
            session.flush()
            session.add_all(item_rows)
            session.commit()

    def set_practice_session_status(self, session_id: str, status: str) -> None:
        with self._session_factory() as session:
            row = session.get(PracticeSessionRow, session_id)
            if row is None:
                raise PracticeSessionNotFoundError(session_id)
            row.status = status
            session.commit()

    def get_practice_session(self, session_id: str) -> PracticeSession | None:
        with self._session_factory() as session:
            row = session.get(PracticeSessionRow, session_id)
            if row is None:
                return None
            return self._load_practice_session(session, row)

    def _load_practice_session(self, session: Session, row: PracticeSessionRow) -> PracticeSession:
        items = list(
            session.scalars(
                select(PracticePassItemRow)
                .where(PracticePassItemRow.session_id == row.id)
                .order_by(PracticePassItemRow.position.asc())
            ).all()
        )
        return _to_session(row, items)

    def list_attempt_keys_for_session(self, session_id: str) -> list[tuple[str, str, str, str]]:
        with self._session_factory() as session:
            rows = session.scalars(
                select(AttemptRow)
                .where(AttemptRow.session_id == session_id)
                .order_by(AttemptRow.created_at.asc(), AttemptRow.id.asc())
            ).all()
            return [(row.id, row.learning_unit_id, row.mode, row.category) for row in rows]

    def advance_current_item(self, session_id: str, position: int) -> int:
        with self._session_factory() as session:
            row = session.get(PracticeSessionRow, session_id)
            if row is None or row.status != OPEN:
                raise PracticeSessionNotFoundError(session_id)
            if row.cursor > position:
                return row.cursor
            if row.cursor != position:
                raise NoCurrentItemError(session_id)
            items = list(
                session.scalars(
                    select(PracticePassItemRow)
                    .where(PracticePassItemRow.session_id == session_id)
                    .order_by(PracticePassItemRow.position.asc())
                ).all()
            )
            item = next((candidate for candidate in items if candidate.position == position), None)
            if item is None:
                raise NoCurrentItemError(session_id)
            attempt = session.scalars(
                select(AttemptRow).where(
                    AttemptRow.session_id == session_id,
                    AttemptRow.learning_unit_id == item.learning_unit_id,
                    AttemptRow.mode == item.mode,
                )
            ).first()
            if attempt is None:
                raise NoCurrentItemError(session_id)
            if position + 1 < len(items):
                row.cursor = position + 1
                session.commit()
                return row.cursor
            definition_count = session.scalar(
                select(func.count())
                .select_from(ExerciseDefinitionRow)
                .where(ExerciseDefinitionRow.generation_id == row.generation_id)
            )
            opening_size = _opening_pass_size(int(definition_count or 0))
            attempts = session.scalars(
                select(AttemptRow)
                .where(AttemptRow.session_id == session_id)
                .order_by(AttemptRow.created_at.asc(), AttemptRow.id.asc())
            ).all()
            categories: dict[tuple[str, str], list[str]] = {}
            for stored in attempts:
                key = (stored.learning_unit_id, stored.mode)
                categories.setdefault(key, []).append(stored.category)
            queue = [
                opening
                for opening in items
                if opening.position < opening_size
                and _still_uncorrected(categories.get((opening.learning_unit_id, opening.mode), []))
            ]
            if not queue:
                row.cursor = position + 1
                session.commit()
                return row.cursor
            start = len(items)
            for offset, opening in enumerate(queue):
                session.add(
                    PracticePassItemRow(
                        id=f"{session_id}:{start + offset}",
                        session_id=session_id,
                        position=start + offset,
                        mode=opening.mode,
                        learning_unit_id=opening.learning_unit_id,
                        definition_id=opening.definition_id,
                    )
                )
            row.cursor = start
            session.commit()
            return row.cursor

    def add_attempt(self, attempt: Attempt, cursor: int) -> None:
        row = AttemptRow(
            id=attempt.id,
            session_id=attempt.session_id,
            learning_unit_id=attempt.learning_unit_id,
            span_start=attempt.span_start,
            span_end=attempt.span_end,
            unit_text=attempt.unit_text,
            mode=attempt.mode,
            submitted=attempt.submitted,
            category=attempt.category,
            expected=attempt.expected,
            explanation=attempt.explanation,
            chunks_used=json.dumps(list(attempt.chunks_used)),
            chunks_missed=json.dumps(list(attempt.chunks_missed)),
            natural_alternative=attempt.natural_alternative,
            created_at=attempt.created_at.isoformat(),
        )
        with self._session_factory() as session:
            stored = session.get(PracticeSessionRow, attempt.session_id)
            if stored is None:
                raise LearningUnitNotFoundError(attempt.session_id)
            session.add(row)
            stored.cursor = cursor
            session.commit()

    def list_attempt_records_for_lesson(self, lesson_id: str) -> list[AttemptRecord]:
        with self._session_factory() as session:
            pairs = session.execute(
                select(AttemptRow, PracticeSessionRow)
                .join(PracticeSessionRow, AttemptRow.session_id == PracticeSessionRow.id)
                .where(PracticeSessionRow.lesson_id == lesson_id)
                .order_by(
                    PracticeSessionRow.created_at.asc(),
                    AttemptRow.created_at.asc(),
                    PracticeSessionRow.id.asc(),
                    AttemptRow.id.asc(),
                )
            ).all()
            session_ids = {practice.id for _attempt, practice in pairs}
            generation_ids = {practice.generation_id for _attempt, practice in pairs}
            item_counts: dict[str, int] = {}
            definition_counts: dict[str, int] = {}
            if session_ids:
                counted = session.execute(
                    select(PracticePassItemRow.session_id, func.count())
                    .where(PracticePassItemRow.session_id.in_(session_ids))
                    .group_by(PracticePassItemRow.session_id)
                ).all()
                item_counts = {session_id: int(count) for session_id, count in counted}
            if generation_ids:
                counted_definitions = session.execute(
                    select(ExerciseDefinitionRow.generation_id, func.count())
                    .where(ExerciseDefinitionRow.generation_id.in_(generation_ids))
                    .group_by(ExerciseDefinitionRow.generation_id)
                ).all()
                definition_counts = {
                    generation_id: int(count) for generation_id, count in counted_definitions
                }
            return [
                AttemptRecord(
                    attempt_id=attempt.id,
                    session_id=practice.id,
                    session_status=practice.status,
                    cursor=practice.cursor,
                    pass_item_count=_listed_pass_size(
                        definition_counts.get(practice.generation_id, 0),
                        item_counts.get(practice.id, 0),
                    ),
                    session_item_count=item_counts.get(practice.id, 0),
                    mode=attempt.mode,
                    category=attempt.category,
                    submitted=attempt.submitted,
                    expected=attempt.expected,
                    explanation=attempt.explanation,
                    chunks_used=_saved_chunks(attempt.chunks_used),
                    chunks_missed=_saved_chunks(attempt.chunks_missed),
                    natural_alternative=attempt.natural_alternative,
                    learning_unit_id=attempt.learning_unit_id,
                    unit_text=attempt.unit_text,
                    span_start=attempt.span_start,
                    span_end=attempt.span_end,
                    created_at=datetime.fromisoformat(attempt.created_at),
                )
                for attempt, practice in pairs
            ]

    def _generation_in_session(
        self, session: Session, row: ExerciseGenerationRow
    ) -> ExerciseGeneration:
        definitions = list(
            session.scalars(
                select(ExerciseDefinitionRow)
                .where(ExerciseDefinitionRow.generation_id == row.id)
                .order_by(ExerciseDefinitionRow.position.asc())
            ).all()
        )
        return _to_generation(row, definitions)


class SqlAlchemyLearningUnitRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def add_unit(self, unit: LearningUnit) -> None:
        row = LearningUnitRow(
            id=unit.id,
            lesson_id=unit.lesson_id,
            span_start=unit.start,
            span_end=unit.end,
            text=unit.text,
            status=unit.status,
            removed_at=None if unit.removed_at is None else unit.removed_at.isoformat(),
            created_at=unit.created_at.isoformat(),
        )
        with self._session_factory() as session:
            session.add(row)
            session.commit()

    def get_unit(self, unit_id: str) -> LearningUnit | None:
        with self._session_factory() as session:
            row = session.get(LearningUnitRow, unit_id)
            if row is None:
                return None
            return _to_unit(row)

    def list_units(self, lesson_id: str) -> list[LearningUnit]:
        statement = (
            select(LearningUnitRow)
            .where(
                LearningUnitRow.lesson_id == lesson_id,
                LearningUnitRow.removed_at.is_(None),
            )
            .order_by(LearningUnitRow.span_start.asc(), LearningUnitRow.id.asc())
        )
        with self._session_factory() as session:
            rows = session.scalars(statement).all()
            return [_to_unit(row) for row in rows]

    def save_unit(self, unit: LearningUnit) -> None:
        with self._session_factory() as session:
            row = session.get(LearningUnitRow, unit.id)
            if row is None:
                raise LearningUnitNotFoundError(unit.id)
            row.status = unit.status
            row.removed_at = None if unit.removed_at is None else unit.removed_at.isoformat()
            session.commit()

    def has_open_practice_session(self, lesson_id: str) -> bool:
        return SqlAlchemyPracticeRepository(self._session_factory).has_open_practice_session(
            lesson_id
        )

    def insert_open_practice_session(
        self, practice: PracticeSession, created_at: datetime
    ) -> PracticeSession:
        return SqlAlchemyPracticeRepository(self._session_factory).insert_open_practice_session(
            practice, created_at
        )

    def get_open_practice_session(self, lesson_id: str) -> PracticeSession | None:
        return SqlAlchemyPracticeRepository(self._session_factory).get_open_practice_session(
            lesson_id
        )

    def latest_completed_generation(self, lesson_id: str) -> ExerciseGeneration | None:
        return SqlAlchemyPracticeRepository(self._session_factory).latest_completed_generation(
            lesson_id
        )

    def list_attempt_records_for_lesson(self, lesson_id: str) -> list[AttemptRecord]:
        return SqlAlchemyPracticeRepository(self._session_factory).list_attempt_records_for_lesson(
            lesson_id
        )


class RepositoryBundle:
    """Lesson, learning-unit, and practice ports over one session factory.

    create_app already stores the object from open_repository. Later commands
    use that same object so app.py stays untouched.
    """

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._lessons = SqlAlchemyLessonRepository(session_factory)
        self._units = SqlAlchemyLearningUnitRepository(session_factory)
        self._practice = SqlAlchemyPracticeRepository(session_factory)

    def add(self, lesson: Lesson) -> None:
        self._lessons.add(lesson)

    def get(self, lesson_id: str) -> Lesson | None:
        return self._lessons.get(lesson_id)

    def list_lessons(self) -> list[Lesson]:
        return self._lessons.list_lessons()

    def add_unit(self, unit: LearningUnit) -> None:
        self._units.add_unit(unit)

    def get_unit(self, unit_id: str) -> LearningUnit | None:
        return self._units.get_unit(unit_id)

    def list_units(self, lesson_id: str) -> list[LearningUnit]:
        return self._units.list_units(lesson_id)

    def save_unit(self, unit: LearningUnit) -> None:
        self._units.save_unit(unit)

    def has_open_practice_session(self, lesson_id: str) -> bool:
        return self._practice.has_open_practice_session(lesson_id)

    def insert_open_practice_session(
        self, practice: PracticeSession, created_at: datetime
    ) -> PracticeSession:
        return self._practice.insert_open_practice_session(practice, created_at)

    def get_open_practice_session(self, lesson_id: str) -> PracticeSession | None:
        return self._practice.get_open_practice_session(lesson_id)

    def save_generation(self, generation: ExerciseGeneration) -> None:
        self._practice.save_generation(generation)

    def latest_completed_generation(self, lesson_id: str) -> ExerciseGeneration | None:
        return self._practice.latest_completed_generation(lesson_id)

    def get_generation(self, generation_id: str) -> ExerciseGeneration | None:
        return self._practice.get_generation(generation_id)

    def save_practice_session(self, practice: PracticeSession, created_at: datetime) -> None:
        self._practice.save_practice_session(practice, created_at)

    def get_practice_session(self, session_id: str) -> PracticeSession | None:
        return self._practice.get_practice_session(session_id)

    def set_practice_session_status(self, session_id: str, status: str) -> None:
        self._practice.set_practice_session_status(session_id, status)

    def list_attempt_keys_for_session(self, session_id: str) -> list[tuple[str, str, str, str]]:
        return self._practice.list_attempt_keys_for_session(session_id)

    def advance_current_item(self, session_id: str, position: int) -> int:
        return self._practice.advance_current_item(session_id, position)

    def add_attempt(self, attempt: Attempt, cursor: int) -> None:
        self._practice.add_attempt(attempt, cursor)

    def list_attempt_records_for_lesson(self, lesson_id: str) -> list[AttemptRecord]:
        return self._practice.list_attempt_records_for_lesson(lesson_id)
