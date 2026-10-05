"""OpenAPI 3.1 operationIds stay aligned with the D-23 command and query names."""

from __future__ import annotations

import json
from pathlib import Path

D23_OPERATION_IDS = frozenset(
    {
        "lesson.create",
        "lesson.get",
        "lesson.list",
        "learning_unit.add",
        "learning_unit.accept",
        "learning_unit.remove",
        "learning_unit.list",
        "exercise.generate",
        "exercise.latest_completed",
        "attempt.list_for_lesson",
        "practice.start",
        "practice.get",
        "practice.finish",
        "practice.start_over",
        "exercise.submit_attempt",
        "exercise_registry.list_visible_for",
        "module_registry.describe",
    }
)


def _operation_ids(schema: dict) -> set[str]:
    ids: set[str] = set()
    for path_item in schema["paths"].values():
        for key, operation in path_item.items():
            if key.startswith("x-") or not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if isinstance(operation_id, str):
                ids.add(operation_id)
    return ids


def test_openapi_operation_ids_match_d23_names(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app

    database_url = f"sqlite:///{(tmp_path / 'openapi.db').as_posix()}"
    schema = create_app(database_url).openapi()
    assert str(schema["openapi"]).startswith("3.1")
    missing = D23_OPERATION_IDS - _operation_ids(schema)
    assert missing == set()


def test_export_openapi_writes_openapi_31_without_secrets(tmp_path: Path) -> None:
    from lait.adapters.http.export_openapi import export_openapi

    destination = tmp_path / "openapi.json"
    written = export_openapi(destination)
    text = written.read_text(encoding="utf-8")
    schema = json.loads(text)
    assert str(schema["openapi"]).startswith("3.1")
    assert D23_OPERATION_IDS <= _operation_ids(schema)
    assert "sk-" not in text
    assert "BEGIN PRIVATE" not in text
    assert "LAIT_DATABASE_URL" not in text
