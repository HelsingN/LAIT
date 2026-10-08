"""Application handlers stay free of FastAPI and SQLAlchemy table metadata (MODL-12).

Independent suites are domain, persistence, modules, and application (PLAT-10).
An empty suite directory must fail collection rather than report success.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
APPLICATION = REPO / "backend" / "lait" / "application"
APPLICATION_TESTS = REPO / "backend" / "tests" / "application"
PERSISTENCE_TESTS = REPO / "backend" / "tests" / "adapters" / "persistence"
SUITE_ROOTS = {
    "domain": REPO / "backend" / "tests" / "domain",
    "persistence": PERSISTENCE_TESTS,
    "modules": REPO / "backend" / "tests" / "modules",
}
SPLIT_COMMAND = (
    "uv run pytest backend/tests/domain backend/tests/adapters/persistence "
    "backend/tests/modules -q"
)
APPLICATION_COMMAND = "uv run pytest backend/tests/application -q"


def _forbidden_module(module: str) -> bool:
    prefixes = (
        "fastapi",
        "sqlalchemy",
        "lait.adapters.http.app",
        "lait.adapters.persistence.models",
    )
    return any(module == prefix or module.startswith(prefix + ".") for prefix in prefixes)


def _import_offenders(root: Path) -> list[str]:
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            for module in modules:
                if _forbidden_module(module):
                    relative = path.relative_to(REPO).as_posix()
                    offenders.append(f"{relative}:{node.lineno}:{module}")
    return offenders


def _cross_suite_offenders(root: Path) -> list[str]:
    needles = (
        "tests.domain",
        "tests.modules",
        "tests.adapters",
        "tests.application",
        "tests.catalog",
    )
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            module = ""
            if isinstance(node, ast.Import):
                module = " ".join(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
            if any(needle in module for needle in needles):
                relative = path.relative_to(REPO).as_posix()
                offenders.append(f"{relative}:{node.lineno}:{module}")
    return offenders


def test_handler_isolation(tmp_path: Path) -> None:
    handler_offenders = _import_offenders(APPLICATION)
    assert handler_offenders == []

    test_offenders = _import_offenders(APPLICATION_TESTS)
    assert test_offenders == []

    for name, root in SUITE_ROOTS.items():
        assert root.is_dir(), name
        tests = list(root.rglob("test_*.py"))
        assert tests, name
        assert _import_offenders(root) == []
        assert _cross_suite_offenders(root) == []

    workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert SPLIT_COMMAND in workflow
    assert APPLICATION_COMMAND in workflow

    empty = tmp_path / "empty_suite"
    empty.mkdir()
    collected = subprocess.run(
        [sys.executable, "-m", "pytest", str(empty), "-q"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert collected.returncode != 0
