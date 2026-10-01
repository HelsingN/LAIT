"""exercise_registry.list_visible_for — exercises whose contribution visibility matches."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from lait.catalog.validation import ModuleRecord

QUERY_NAME = "exercise_registry.list_visible_for"


@dataclass(frozen=True, slots=True)
class VisibleExercise:
    exercise_type: str
    visibility: str
    module_id: str


def handle(audience: str, registry: Sequence[ModuleRecord]) -> list[VisibleExercise]:
    rows = [
        VisibleExercise(
            exercise_type=module.contribution.exercise_type,
            visibility=module.contribution.visibility,
            module_id=module.module_id,
        )
        for module in registry
        if module.contribution is not None and module.contribution.visibility == audience
    ]
    rows.sort(key=lambda row: row.module_id)
    return rows
