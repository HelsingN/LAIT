"""Removing the proof catalog entry leaves Gap Fill working (MODL-03, D-20).

The overlay is a temp copy of bundled manifests with the proof entry omitted.
Default catalog files, Core domain, and application handlers stay untouched.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MODULES = REPO / "backend" / "lait" / "modules"
PROOF_MANIFEST = MODULES / "exercise_proof" / "manifest.json"
CORE_ROOTS = (
    REPO / "backend" / "lait" / "domain",
    REPO / "backend" / "lait" / "application",
)


def _digest(root: Path) -> str:
    hasher = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        hasher.update(path.relative_to(root).as_posix().encode())
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def _core_digests() -> dict[str, str]:
    return {root.relative_to(REPO).as_posix(): _digest(root) for root in CORE_ROOTS}


def _overlay_without_proof(tmp_path: Path) -> Path:
    overlay = tmp_path / "modules"
    overlay.mkdir()
    for manifest in MODULES.glob("*/manifest.json"):
        if manifest.parent.name == "exercise_proof":
            continue
        destination = overlay / manifest.parent.name
        destination.mkdir()
        shutil.copyfile(manifest, destination / "manifest.json")
    return overlay


def test_proof_removal(tmp_path: Path, monkeypatch) -> None:
    from fastapi.testclient import TestClient

    from lait.adapters.http.app import create_app
    from lait.adapters.persistence.database import migrate
    from lait.application.commands.exercise_generate import ExerciseGenerate
    from lait.application.commands.exercise_generate import handle as generate
    from lait.application.commands.learning_unit_accept import LearningUnitAccept
    from lait.application.commands.learning_unit_accept import handle as accept_unit
    from lait.application.commands.learning_unit_add import LearningUnitAdd
    from lait.application.commands.learning_unit_add import handle as add_unit
    from lait.application.commands.lesson_create import LessonCreate
    from lait.application.commands.lesson_create import handle as create_lesson
    from lait.catalog.loader import load_bundled_catalog

    before = _core_digests()
    assert PROOF_MANIFEST.is_file()
    default_types = {
        record.contribution.exercise_type
        for record in load_bundled_catalog()
        if record.contribution is not None
    }
    assert "proof" in default_types
    assert "gap-fill" in default_types

    overlay = _overlay_without_proof(tmp_path)
    assert not (overlay / "exercise_proof").exists()
    assert (overlay / "exercise_gap_fill" / "manifest.json").is_file()
    monkeypatch.setattr(
        "lait.catalog.loader.bundled_manifest_paths",
        lambda: tuple(sorted(overlay.glob("*/manifest.json"))),
    )

    database_url = f"sqlite:///{(tmp_path / 'proof-removal.db').as_posix()}"
    migrate(database_url)
    app = create_app(database_url)
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}

    described = client.get("/api/module-registry")
    assert described.status_code == 200
    modules = described.json()["modules"]
    described_types = {row["exercise_type"] for row in modules}
    assert "proof" not in described_types
    assert "gap-fill" in described_types
    assert {row["activation_status"] for row in modules} == {"active"}

    learner = client.get("/api/exercise-registry", params={"visibility": "learner"})
    assert learner.status_code == 200
    exercises = learner.json()["exercises"]
    assert [row["exercise_type"] for row in exercises] == ["gap-fill"]
    assert [row["visibility"] for row in exercises] == ["learner"]

    source = "I was responsible for rolling out the migration."
    repository = app.state.lesson_repository
    lesson = create_lesson(LessonCreate(source=source), repository)
    start = source.index("rolling out")
    created = add_unit(
        LearningUnitAdd(lesson_id=lesson.id, start=start, end=start + len("rolling out")),
        repository,
        repository,
    )
    accept_unit(
        LearningUnitAccept(lesson_id=lesson.id, unit_id=created.id),
        repository,
        repository,
    )
    outcome = generate(
        ExerciseGenerate(lesson_id=lesson.id),
        repository,
        repository,
        app.state.module_registry,
    )
    assert outcome.status == "completed"
    assert outcome.definition_count == 1

    assert PROOF_MANIFEST.is_file()
    assert _core_digests() == before
    for root in CORE_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "exercise_proof" not in text
            assert "ProofRenderer" not in text

    readme = (REPO / "README.md").read_text(encoding="utf-8")
    marker = "## Removing the proof exercise"
    assert marker in readme
    section = readme.split(marker, 1)[1].split("\n## ", 1)[0]
    assert "backend/lait/modules/exercise_proof/manifest.json" in section
    assert "frontend/src/registries/renderers/registry.ts" in section
    assert "ProofRenderer" in section
    assert "backend/lait/domain" in section
    assert "backend/lait/application" in section
