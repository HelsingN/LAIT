"""module_registry.describe returns public active rows only."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

PUBLIC_FIELDS = {
    "module_id",
    "module_version",
    "category",
    "capabilities",
    "exercise_type",
    "visibility",
    "activation_status",
}


def _database_url(tmp_path: Path) -> str:
    return f"sqlite:///{(tmp_path / 'describe.db').as_posix()}"


def test_describe_returns_public_active_rows() -> None:
    from lait.application.queries.module_registry_describe import QUERY_NAME, handle
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    assert QUERY_NAME == "module_registry.describe"
    rows = handle(validate_catalog(load_bundled_catalog()))
    assert [row.module_id for row in rows] == [
        "official.exercise.gap-fill",
        "official.exercise.proof",
    ]
    by_id = {row.module_id: row for row in rows}
    gap = by_id["official.exercise.gap-fill"]
    proof = by_id["official.exercise.proof"]
    assert set(gap.__dataclass_fields__) == PUBLIC_FIELDS
    assert gap.activation_status == "active"
    assert proof.activation_status == "active"
    assert gap.category == "exercise"
    assert proof.category == "exercise"
    assert gap.module_version == "0.1.0"
    assert proof.module_version == "0.1.0"
    assert gap.exercise_type == "gap-fill"
    assert gap.visibility == "learner"
    assert proof.exercise_type == "proof"
    assert proof.visibility == "maintainer"
    assert gap.capabilities == ("exercise.generate", "exercise.evaluate")
    assert proof.capabilities == ("exercise.generate", "exercise.evaluate")
    for banned in ("source_path", "entrypoint", "publisher", "dependencies", "name"):
        assert banned not in gap.__dataclass_fields__


def test_http_module_registry_maps_describe(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from lait.adapters.http.app import create_app

    client = TestClient(create_app(_database_url(tmp_path)))
    response = client.get("/api/module-registry")
    assert response.status_code == 200
    modules = response.json()["modules"]
    assert [row["module_id"] for row in modules] == [
        "official.exercise.gap-fill",
        "official.exercise.proof",
    ]
    assert modules[0]["activation_status"] == "active"
    assert modules[0]["visibility"] == "learner"
    assert modules[1]["visibility"] == "maintainer"
    assert set(modules[0]) == PUBLIC_FIELDS

    router_path = REPO / "backend/lait/adapters/http/routers/diagnostics.py"
    router = router_path.read_text(encoding="utf-8")
    assert "adapters.persistence" not in router
    assert "lesson_repository" not in router
    assert "sqlalchemy" not in router.lower()


def test_describe_query_does_not_import_modules_or_fastapi() -> None:
    source = (
        REPO / "backend/lait/application/queries/module_registry_describe.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    assert "exercise_gap_fill" not in source
    assert "exercise_proof" not in source
    assert "fastapi" not in lowered
    assert "sqlalchemy" not in lowered
