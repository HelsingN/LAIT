"""Proof exercise uses the public generate/evaluate contract and stays unlisted."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

_BANNED_IN_CORE = (
    "exercise_gap_fill",
    "exercise_proof",
    "official.exercise.gap-fill",
    "official.exercise.proof",
)


def _repo() -> Path:
    return Path(__file__).resolve().parents[4]


def _assert_public_protocol(generate, evaluate, exercise_type: str) -> None:
    from lait.domain.exercise import (
        RESULT_CATEGORIES,
        AcceptedUnit,
        DragAnswer,
        Evaluation,
        GenerateResult,
        TypedAnswer,
    )

    assert list(inspect.signature(generate).parameters) == ["source", "units"]
    assert list(inspect.signature(evaluate).parameters) == ["item", "answer"]

    source = "alpha beta."
    result = generate(
        source,
        [
            AcceptedUnit(learning_unit_id="b", start=6, end=10, text="beta"),
            AcceptedUnit(learning_unit_id="a", start=0, end=5, text="alpha"),
        ],
    )
    assert isinstance(result, GenerateResult)
    assert [item.learning_unit_id for item in result.items] == ["a", "b"]
    assert [item.exercise_type for item in result.items] == [exercise_type, exercise_type]
    assert result.chip_unit_ids == ("a", "b")

    item = result.items[0]
    drag_hit = evaluate(
        item,
        DragAnswer(learning_unit_id=item.learning_unit_id, text=item.target_text),
    )
    drag_miss = evaluate(item, DragAnswer(learning_unit_id="other", text=item.target_text))
    typed = evaluate(item, TypedAnswer("nope"))
    assert drag_hit.category == "correct"
    assert drag_miss.category == "incorrect"
    for graded in (drag_hit, drag_miss, typed):
        assert isinstance(graded, Evaluation)
        assert graded.category in RESULT_CATEGORIES
        assert graded.explanation != ""
        assert graded.natural_alternative is None or isinstance(graded.natural_alternative, str)
        assert isinstance(graded.chunks_used, tuple)
        assert isinstance(graded.chunks_missed, tuple)


def test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill() -> None:
    repo = _repo()
    gap_manifest = json.loads(
        (repo / "backend/lait/modules/exercise_gap_fill/manifest.json").read_text(encoding="utf-8")
    )
    proof_manifest = json.loads(
        (repo / "backend/lait/modules/exercise_proof/manifest.json").read_text(encoding="utf-8")
    )
    assert proof_manifest["category"] == "exercise"
    assert proof_manifest["capabilities"] == ["exercise.generate", "exercise.evaluate"]
    assert gap_manifest["capabilities"] == proof_manifest["capabilities"]
    assert gap_manifest["dependencies"] == proof_manifest["dependencies"]
    assert gap_manifest["api_version"] == proof_manifest["api_version"]

    from lait.modules.exercise_gap_fill.evaluate import evaluate as gap_evaluate
    from lait.modules.exercise_gap_fill.generate import generate as gap_generate
    from lait.modules.exercise_proof.contribution import CONTRIBUTION
    from lait.modules.exercise_proof.evaluate import evaluate as proof_evaluate
    from lait.modules.exercise_proof.generate import generate as proof_generate

    assert CONTRIBUTION.exercise_type == "proof"
    assert CONTRIBUTION.visibility == "maintainer"
    proof_generate_source = Path(inspect.getfile(proof_generate)).read_text(encoding="utf-8")
    proof_evaluate_source = Path(inspect.getfile(proof_evaluate)).read_text(encoding="utf-8")
    assert "exercise_gap_fill" not in proof_generate_source
    assert "exercise_gap_fill" not in proof_evaluate_source

    _assert_public_protocol(proof_generate, proof_evaluate, "proof")
    _assert_public_protocol(gap_generate, gap_evaluate, "gap-fill")


def test_core_does_not_special_case_exercise_module_ids() -> None:
    repo = _repo()
    roots = (
        repo / "backend/lait/domain",
        repo / "backend/lait/application",
        repo / "backend/lait/adapters",
        repo / "backend/lait/catalog",
    )
    for root in roots:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for banned in _BANNED_IN_CORE:
                assert banned not in text, f"{path} mentions {banned}"
