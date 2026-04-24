"""Self-bootstrap layout checks for packaged multi-root emits."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.a1_at_functions.assimilate_policy_gate import load_and_validate_assimilate_policy
from ass_ade.a3_og_features.pipeline_book import run_book_until

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_checked_self_assimilate_policy_validates() -> None:
    policy_path = _REPO_ROOT / ".ass-ade" / "policies" / "self-assimilate.yaml"
    doc = load_and_validate_assimilate_policy(policy_path)
    assert doc["primary"]["path"] == "ass-ade-v1.1"
    assert any(str(row.get("path")) == "atomadic-engine" for row in doc["roots"])


@pytest.mark.usecase
def test_multi_root_src_layout_emits_prefixed_package_tree(tmp_path: Path) -> None:
    cross_app = _FIXTURES / "cross_app"
    cross_lib = _FIXTURES / "cross_lib"
    book = run_book_until(
        cross_app,
        tmp_path,
        extra_source_roots=[cross_lib],
        stop_after=7,
        rebuild_tag="src-layout",
        distribution_name="ass-ade-assimilated",
        output_package_name="ass_ade",
    )
    assert book["stopped_after"] == 7
    assert book["phase6"]["audit"]["summary"]["structure_conformant"] is True

    target_root = Path(book["phase5"]["target_root"])
    package_root = Path(book["phase5"]["package_root"])
    assert package_root == target_root / "src" / "ass_ade"

    entry = package_root / "a1_at_functions" / "a1_source_cross_app_run_add.py"
    assert entry.is_file()
    text = entry.read_text(encoding="utf-8")
    assert "from ass_ade.a1_at_functions.a1_source_cross_lib_add_one import add_one" in text

    pyproject = (target_root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'package-dir = {"" = "src"}' in pyproject
    assert 'root_package = "ass_ade"' in pyproject

    manifest_path = target_root / "tests" / "generated_smoke" / "_qualnames.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "ass_ade.a1_at_functions.a1_source_cross_app_run_add" in manifest
