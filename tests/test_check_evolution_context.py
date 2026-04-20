"""Tier a1 — evolution context gate (researchRadar REFINE + evidence)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_evolution_context.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_evolution_context", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cec = _load_module()


def test_not_refine_ok() -> None:
    ok, msgs = cec.check(
        doc={"researchRadar": {"verdict": "PASS", "refinementProgress": []}},
        git_range=None,
        repo=Path("."),
    )
    assert ok and not msgs


def test_refine_empty_progress_fails() -> None:
    ok, msgs = cec.check(
        doc={"researchRadar": {"verdict": "REFINE", "refinementProgress": []}},
        git_range=None,
        repo=Path("."),
    )
    assert not ok and msgs


def test_refine_missing_evidence_strings_fails() -> None:
    ok, msgs = cec.check(
        doc={
            "researchRadar": {
                "verdict": "REFINE",
                "refinementProgress": [{"id": "x", "status": "done"}],
            }
        },
        git_range=None,
        repo=Path("."),
    )
    assert not ok and msgs


def test_refine_with_evidence_ok_without_git() -> None:
    ok, msgs = cec.check(
        doc={
            "researchRadar": {
                "verdict": "REFINE",
                "refinementProgress": [
                    {"id": "x", "status": "done", "evidence": "tests/test_mcp_foo.py"}
                ],
            }
        },
        git_range=None,
        repo=Path("."),
    )
    assert ok and not msgs


def test_mcp_paths_and_manifest_evidence_matching() -> None:
    assert cec._mcp_evolution_paths(["mcp/server.json", "README.md"]) == ["mcp/server.json"]
    assert cec._mcp_evolution_paths(["src/ass_ade/mcp/server.py"]) == ["src/ass_ade/mcp/server.py"]
    blob_bad = "tests/test_mcp_only.py".lower()
    assert not cec._evidence_covers_change(blob_bad, "mcp/server.json")
    blob_ok = "mcp/server.json and ci".lower()
    assert cec._evidence_covers_change(blob_ok, "mcp/server.json")
    blob_py = "tests/test_mcp_research_radar_fixture.py".lower()
    assert cec._evidence_covers_change(blob_py, "src/ass_ade/mcp/server.py")
