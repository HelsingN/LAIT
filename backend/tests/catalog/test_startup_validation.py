"""Startup refuses an invalid static catalog and serves a valid one."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]


def _database_url(tmp_path: Path) -> str:
    return f"sqlite:///{(tmp_path / 'catalog.db').as_posix()}"


def _entry(
    *,
    module_id: str = "official.exercise.gap-fill",
    exercise_type: str = "gap-fill",
    visibility: str = "learner",
    dependencies: list[str] | None = None,
    extra_manifest: dict | None = None,
    omit_contribution_fields: tuple[str, ...] = (),
) -> dict:
    manifest = {
        "module_id": module_id,
        "name": "Gap Fill",
        "module_version": "0.1.0",
        "api_version": 1,
        "publisher": "ai-language-coach",
        "category": "exercise",
        "capabilities": ["exercise.generate", "exercise.evaluate"],
        "dependencies": ["core.exercise-api>=0.1.0"] if dependencies is None else dependencies,
    }
    if extra_manifest:
        manifest.update(extra_manifest)
    contribution = {"exercise_type": exercise_type, "visibility": visibility}
    for field in omit_contribution_fields:
        contribution.pop(field, None)
    return {"manifest": manifest, "contribution": contribution}


def test_visibility_on_universal_manifest_refuses_startup(tmp_path: Path) -> None:
    from lait.catalog.validation import CatalogInvalidError

    from lait.adapters.http.app import create_app

    entry = _entry(extra_manifest={"visibility": "learner"})
    with pytest.raises(CatalogInvalidError) as caught:
        create_app(_database_url(tmp_path), catalog_entries=[entry])
    assert caught.value.code == "invalid_manifest"


def test_duplicate_module_id_refuses_startup(tmp_path: Path) -> None:
    from lait.catalog.validation import CatalogInvalidError

    from lait.adapters.http.app import create_app

    entries = [
        _entry(module_id="official.exercise.gap-fill", exercise_type="gap-fill"),
        _entry(
            module_id="official.exercise.gap-fill",
            exercise_type="proof",
            visibility="maintainer",
        ),
    ]
    with pytest.raises(CatalogInvalidError) as caught:
        create_app(_database_url(tmp_path), catalog_entries=entries)
    assert caught.value.code == "duplicate_module_id"


def test_unresolved_dependency_refuses_startup(tmp_path: Path) -> None:
    from lait.catalog.validation import CatalogInvalidError

    from lait.adapters.http.app import create_app

    entry = _entry(dependencies=["missing.module>=0.1.0"])
    with pytest.raises(CatalogInvalidError) as caught:
        create_app(_database_url(tmp_path), catalog_entries=[entry])
    assert caught.value.code == "unresolved_dependency"


def test_experimental_visibility_is_rejected(tmp_path: Path) -> None:
    from lait.catalog.validation import CatalogInvalidError

    from lait.adapters.http.app import create_app

    entry = _entry(visibility="experimental")
    with pytest.raises(CatalogInvalidError) as caught:
        create_app(_database_url(tmp_path), catalog_entries=[entry])
    assert caught.value.code == "invalid_visibility"


def test_bundled_catalog_starts(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from lait.adapters.http.app import create_app

    client = TestClient(create_app(_database_url(tmp_path)))
    assert client.get("/health").status_code == 200


def test_universal_manifests_and_schema_omit_visibility() -> None:
    from lait.catalog.loader import bundled_manifest_paths, manifest_schema_path

    schema = json.loads(manifest_schema_path().read_text(encoding="utf-8"))
    assert "visibility" not in schema["properties"]
    assert schema["additionalProperties"] is False
    paths = list(bundled_manifest_paths())
    assert {path.parent.name for path in paths} == {"exercise_gap_fill", "exercise_proof"}
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        assert "visibility" not in document
        assert document["category"] == "exercise"
