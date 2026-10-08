"""Validate a static catalog before the process serves requests."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, ValidationError

LIVE_VISIBILITY = frozenset({"learner", "maintainer"})
SUPPORTED_API_VERSION = 1
CORE_APIS: dict[str, tuple[int, ...]] = {"core.exercise-api": (0, 1, 0)}

_DEPENDENCY = re.compile(r"^(\S+?)(?:\s*>=\s*(\d+(?:\.\d+)*))?$")


class CatalogInvalidError(Exception):
    """Raised when bundled manifests must not be served."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class ModuleManifestModel(BaseModel):
    """Universal manifest. Visibility is not a field (D-21)."""

    model_config = ConfigDict(extra="forbid")

    module_id: str = Field(min_length=1)
    name: str | None = None
    module_version: str = Field(min_length=1)
    api_version: int
    publisher: str | None = None
    category: str = Field(pattern="^exercise$")
    capabilities: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)
    dependencies: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ExerciseContribution:
    exercise_type: str
    visibility: str


@dataclass(frozen=True, slots=True)
class ModuleRecord:
    module_id: str
    module_version: str
    api_version: int
    category: str
    capabilities: tuple[str, ...]
    dependencies: tuple[str, ...]
    contribution: ExerciseContribution | None
    package: str = ""


def parse_catalog_entry(entry: dict) -> ModuleRecord:
    manifest = entry.get("manifest")
    if not isinstance(manifest, dict):
        raise CatalogInvalidError("invalid_manifest", "manifest must be an object")
    try:
        parsed = ModuleManifestModel.model_validate(manifest)
    except ValidationError as exc:
        raise CatalogInvalidError("invalid_manifest", "manifest failed schema validation") from exc
    if parsed.api_version != SUPPORTED_API_VERSION:
        raise CatalogInvalidError("api_incompatible", "module API version is not supported")
    contribution = _parse_contribution(entry.get("contribution"), parsed.category)
    raw_package = entry.get("package", "")
    package = raw_package if isinstance(raw_package, str) else ""
    return ModuleRecord(
        module_id=parsed.module_id,
        module_version=parsed.module_version,
        api_version=parsed.api_version,
        category=parsed.category,
        capabilities=tuple(parsed.capabilities),
        dependencies=tuple(parsed.dependencies),
        contribution=contribution,
        package=package,
    )


def validate_catalog(modules: Sequence[ModuleRecord]) -> tuple[ModuleRecord, ...]:
    if len(modules) == 0:
        raise CatalogInvalidError("empty_catalog", "catalog has no modules")
    seen: dict[str, ModuleRecord] = {}
    for module in modules:
        if module.module_id in seen:
            raise CatalogInvalidError(
                "duplicate_module_id",
                f"duplicate module_id {module.module_id}",
            )
        seen[module.module_id] = module
    for module in modules:
        for spec in module.dependencies:
            if not _dependency_resolves(spec, seen):
                raise CatalogInvalidError(
                    "unresolved_dependency",
                    f"unresolved dependency {spec}",
                )
    return tuple(modules)


def _parse_contribution(raw: object, category: str) -> ExerciseContribution | None:
    if isinstance(raw, ExerciseContribution):
        raw = {"exercise_type": raw.exercise_type, "visibility": raw.visibility}
    if category == "exercise":
        if not isinstance(raw, dict):
            raise CatalogInvalidError("invalid_manifest", "exercise module requires a contribution")
        visibility = raw.get("visibility")
        if visibility not in LIVE_VISIBILITY:
            raise CatalogInvalidError(
                "invalid_visibility",
                "visibility must be learner or maintainer",
            )
        exercise_type = raw.get("exercise_type")
        if not isinstance(exercise_type, str) or exercise_type.strip() == "":
            raise CatalogInvalidError("missing_contribution_field", "exercise_type is required")
        return ExerciseContribution(exercise_type=exercise_type, visibility=str(visibility))
    if raw is not None:
        raise CatalogInvalidError("invalid_manifest", "contribution is exercise metadata only")
    return None


def _dependency_resolves(spec: str, modules: dict[str, ModuleRecord]) -> bool:
    match = _DEPENDENCY.fullmatch(spec.strip())
    if match is None:
        return False
    name, required = match.group(1), match.group(2)
    required_version = _version_tuple(required) if required is not None else None
    if name in CORE_APIS:
        if required_version is None:
            return True
        return _version_satisfies(CORE_APIS[name], required_version)
    module = modules.get(name)
    if module is None:
        return False
    if required_version is None:
        return True
    return _version_satisfies(_version_tuple(module.module_version), required_version)


def _version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def _version_satisfies(actual: tuple[int, ...], required: tuple[int, ...]) -> bool:
    width = max(len(actual), len(required))
    actual_wide = actual + (0,) * (width - len(actual))
    required_wide = required + (0,) * (width - len(required))
    return actual_wide >= required_wide
