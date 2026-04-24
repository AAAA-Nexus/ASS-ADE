from __future__ import annotations

import json
from pathlib import Path

from ass_ade.a1_at_functions.test_synth_plan import (
    list_expected_qualnames,
    plan_manifest_payload,
    qualname_for_src_py,
)


def test_qualname_for_package_init() -> None:
    repo = Path(__file__).resolve().parents[1]
    p = repo / "src" / "ass_ade" / "__init__.py"
    assert qualname_for_src_py(p, repo) == "ass_ade"


def test_expected_qualnames_include_core() -> None:
    root = Path(__file__).resolve().parents[1]
    names = list_expected_qualnames(root)
    assert "ass_ade" in names
    assert "ass_ade.a1_at_functions.ingest" in names
    assert "ass_ade.a4_sy_orchestration.cli" in names


def test_plan_manifest_payload_matches_expected_list(repo_root: Path) -> None:
    text = plan_manifest_payload(repo_root)
    assert text.endswith("\n")
    data = json.loads(text)
    assert data == list_expected_qualnames(repo_root)
