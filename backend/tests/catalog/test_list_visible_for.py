"""exercise_registry.list_visible_for filters on contribution visibility."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def _database_url(tmp_path: Path) -> str:
    return f"sqlite:///{(tmp_path / 'visible.db').as_posix()}"


def test_learner_list_includes_gap_fill_and_omits_proof() -> None:
    from lait.application.queries.exercise_registry_list_visible import QUERY_NAME, handle
    from lait.catalog.loader import load_bundled_catalog
    from lait.catalog.validation import validate_catalog

    assert QUERY_NAME == "exercise_registry.list_visible_for"
    registry = validate_catalog(load_bundled_catalog())
    learner = handle("learner", registry)
    assert [row.exercise_type for row in learner] == ["gap-fill"]
    assert [row.visibility for row in learner] == ["learner"]
    assert "proof" not in {row.exercise_type for row in learner}
    maintainer = handle("maintainer", registry)
    assert [row.exercise_type for row in maintainer] == ["proof"]
    assert [row.visibility for row in maintainer] == ["maintainer"]

    source = (
        REPO / "backend/lait/application/queries/exercise_registry_list_visible.py"
    ).read_text(encoding="utf-8")
    assert "gap-fill" not in source
    assert "official.exercise" not in source
    assert "exercise_proof" not in source
    assert "exercise_gap_fill" not in source


def test_http_exercise_registry_learner_returns_gap_fill_only(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from lait.adapters.http.app import create_app

    client = TestClient(create_app(_database_url(tmp_path)))
    response = client.get("/api/exercise-registry", params={"visibility": "learner"})
    assert response.status_code == 200
    exercises = response.json()["exercises"]
    assert [row["exercise_type"] for row in exercises] == ["gap-fill"]
    assert exercises[0]["visibility"] == "learner"
    assert "proof" not in {row["exercise_type"] for row in exercises}
    assert set(exercises[0]) == {"exercise_type", "visibility", "module_id"}


def test_lesson_feature_does_not_call_module_registry_describe() -> None:
    lesson = REPO / "frontend/src/features/lesson"
    assert lesson.is_dir()
    for path in lesson.rglob("*"):
        if path.suffix not in {".ts", ".tsx"}:
            continue
        text = path.read_text(encoding="utf-8")
        assert "/api/module-registry" not in text
        assert "module_registry.describe" not in text

    lessons_router = (REPO / "backend/lait/adapters/http/routers/lessons.py").read_text(
        encoding="utf-8"
    )
    assert "module_registry" not in lessons_router
    assert "/api/module-registry" not in lessons_router
