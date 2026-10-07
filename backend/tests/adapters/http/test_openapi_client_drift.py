"""PLAT-09: the committed TypeScript client matches OpenAPI, and CI fails on drift."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
GENERATED_SDK = REPO / "frontend" / "src" / "api" / "generated" / "sdk.gen.ts"
LESSON_API = REPO / "frontend" / "src" / "features" / "lesson" / "lessonApi.ts"
HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete"})


def _export_name(operation_id: str) -> str:
    tokens = [token for token in re.split(r"[._]", operation_id) if token]
    head, *tail = tokens
    return head + "".join(token[:1].upper() + token[1:] for token in tail)


def _operations(schema: dict) -> list[tuple[str, str, str]]:
    found: list[tuple[str, str, str]] = []
    for path, path_item in schema["paths"].items():
        for method, operation in path_item.items():
            if method not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            assert isinstance(operation_id, str) and operation_id
            found.append((method, path, operation_id))
    return found


def test_typescript_client_matches_openapi_and_ci_rejects_drift(tmp_path: Path) -> None:
    from lait.adapters.http.app import create_app

    database_url = f"sqlite:///{(tmp_path / 'openapi-client.db').as_posix()}"
    schema = create_app(database_url).openapi()
    assert str(schema["openapi"]).startswith("3.1")

    sdk = GENERATED_SDK.read_text(encoding="utf-8")
    lesson_api = LESSON_API.read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    package = json.loads((REPO / "frontend" / "package.json").read_text(encoding="utf-8"))
    generator = (REPO / "frontend" / "scripts" / "openapi-generate.mjs").read_text(
        encoding="utf-8"
    )

    missing_exports: list[str] = []
    missing_routes: list[str] = []
    for method, path, operation_id in _operations(schema):
        export_name = _export_name(operation_id)
        if f"export const {export_name} " not in sdk:
            missing_exports.append(f"{operation_id} -> {export_name}")
        needle = f".{method}<" if f".{method}<" in sdk else f".{method}("
        if f"url: '{path}'" not in sdk or needle not in sdk:
            missing_routes.append(f"{method.upper()} {path}")

    assert missing_exports == []
    assert missing_routes == []
    assert "sk-" not in sdk
    assert "LAIT_DATABASE_URL" not in sdk
    assert 'from "../../api/generated/index.ts"' in lesson_api
    assert "lessonCreate" in lesson_api
    assert package["devDependencies"]["@hey-api/openapi-ts"] == "0.99.0"
    assert "partial client must leave the tree dirty" in generator
    assert "uv run python -m lait.adapters.http.export_openapi" in workflow
    assert "npm --prefix frontend run openapi:generate" in workflow
    assert "git diff --exit-code -- frontend/src/api/generated" in workflow
