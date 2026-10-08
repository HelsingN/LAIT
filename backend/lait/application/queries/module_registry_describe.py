"""module_registry.describe — public registry metadata for a live catalog."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from lait.catalog.validation import ModuleRecord

QUERY_NAME = "module_registry.describe"


@dataclass(frozen=True, slots=True)
class ModuleDescription:
    module_id: str
    module_version: str
    category: str
    capabilities: tuple[str, ...]
    exercise_type: str
    visibility: str
    activation_status: str


def handle(registry: Sequence[ModuleRecord]) -> list[ModuleDescription]:
    rows = [
        ModuleDescription(
            module_id=module.module_id,
            module_version=module.module_version,
            category=module.category,
            capabilities=module.capabilities,
            exercise_type="" if module.contribution is None else module.contribution.exercise_type,
            visibility="" if module.contribution is None else module.contribution.visibility,
            activation_status="active",
        )
        for module in registry
    ]
    rows.sort(key=lambda row: (row.category, row.module_id))
    return rows
