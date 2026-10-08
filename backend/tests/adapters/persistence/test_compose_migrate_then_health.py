"""PLAT-03: the documented Compose command is healthy only after migrations."""

from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
ENTRYPOINT = REPO / "docker" / "api_entrypoint.py"


def _entrypoint():
    spec = importlib.util.spec_from_file_location("lait_api_entrypoint", ENTRYPOINT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tables(database: Path) -> set[str]:
    connection = sqlite3.connect(database)
    try:
        rows = connection.execute(
            "select name from sqlite_master where type = 'table'"
        )
        return {name for (name,) in rows}
    finally:
        connection.close()


def test_api_process_migrates_before_health_can_be_served(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database = tmp_path / "lait.db"
    monkeypatch.setenv("LAIT_DATABASE_URL", f"sqlite:///{database.as_posix()}")
    module = _entrypoint()
    served: list[tuple[str, list[str]]] = []

    def fake_execvp(file: str, args: list[str]) -> None:
        # uvicorn is not running yet. /health cannot answer until this call.
        tables = _tables(database)
        assert "alembic_version" in tables
        assert "lessons" in tables
        served.append((file, list(args)))

    monkeypatch.setattr(module.os, "execvp", fake_execvp)
    module.main()

    assert served == [
        (
            "uvicorn",
            [
                "uvicorn",
                "lait.adapters.http.app:create_app",
                "--factory",
                "--app-dir",
                "backend",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
        )
    ]


def test_missing_database_url_exits_before_the_server_starts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("LAIT_DATABASE_URL", raising=False)
    module = _entrypoint()
    monkeypatch.setattr(
        module.os,
        "execvp",
        lambda *_args: pytest.fail("server started without a database url"),
    )

    with pytest.raises(SystemExit) as caught:
        module.main()

    assert caught.value.code == 1


def test_compose_waits_for_health_after_the_migrating_entrypoint() -> None:
    compose = (REPO / "docker-compose.yml").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    dockerfile = (REPO / "Dockerfile.api").read_text(encoding="utf-8")
    workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "docker compose up -d --wait" in readme
    assert "docker compose up -d --wait" in workflow
    assert "docker compose down -v" in readme
    assert 'ENTRYPOINT ["python", "/usr/local/bin/api_entrypoint.py"]' in dockerfile
    assert "http://127.0.0.1:8000/health" in compose
    assert "condition: service_healthy" in compose
    assert "sqlite:////app/data/lait.db" in compose
    assert "app-data:" in compose
