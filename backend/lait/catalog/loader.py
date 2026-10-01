"""Load build-time bundled manifests.

Manifest entrypoints are not executed. Contribution metadata is imported from
the bundled package that sits next to each manifest.json.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from lait.catalog.validation import ExerciseContribution, ModuleRecord, parse_catalog_entry

_MODULES_PACKAGE = "lait.modules"


def manifest_schema_path() -> Path:
    return Path(__file__).resolve().parent / "manifests" / "module-manifest.schema.json"


def bundled_manifest_paths() -> tuple[Path, ...]:
    modules_root = Path(__file__).resolve().parents[1] / "modules"
    return tuple(sorted(modules_root.glob("*/manifest.json")))


def load_bundled_catalog() -> list[ModuleRecord]:
    records: list[ModuleRecord] = []
    for manifest_path in bundled_manifest_paths():
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        contribution = _load_contribution(manifest_path.parent.name)
        records.append(parse_catalog_entry({"manifest": document, "contribution": contribution}))
    return records


def _load_contribution(package: str) -> dict[str, str] | ExerciseContribution:
    module_name = f"{_MODULES_PACKAGE}.{package}.contribution"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise CatalogLoadError(f"bundled module {package} has no contribution") from exc
    contribution = getattr(module, "CONTRIBUTION", None)
    if isinstance(contribution, ExerciseContribution):
        return contribution
    if isinstance(contribution, dict):
        return contribution
    raise CatalogLoadError(f"bundled module {package} contribution is missing")


class CatalogLoadError(Exception):
    """A bundled package is not a static catalog entry."""
