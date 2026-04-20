"""Tests for GitHub evolution control gate (stdlib + mocked gh)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]


def _load_gec():
    path = _REPO / "scripts" / "github_evolution_control.py"
    spec = importlib.util.spec_from_file_location("_github_evolution_control", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_gate_lane_disabled_writes_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = {
        "schemaVersion": "ass-ade.github-evolution-control.v1",
        "global": {"evolutionBranchPrefix": "auto-evolve/", "maxOpenEvolutionPrs": 5},
        "lanes": {"cycle": {"enabled": False}},
    }
    root = tmp_path / "repo"
    (root / ".ass-ade").mkdir(parents=True)
    (root / ".ass-ade" / "github-evolution-control.json").write_text(json.dumps(cfg), encoding="utf-8")
    out_file = tmp_path / "gh_out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")

    gec = _load_gec()
    monkeypatch.setattr(gec, "_repo_root", lambda: root)
    assert gec.cmd_gate("cycle", root) == 0
    text = out_file.read_text(encoding="utf-8")
    assert "proceed=false" in text
    assert "lane_disabled" in text


def test_gate_global_cap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _REPO
    out_file = tmp_path / "gh_out.txt"
    out_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("GITHUB_TOKEN", "tok")

    fake_heads = '[{"headRefName":"auto-evolve/a"},{"headRefName":"auto-evolve/b"}]'

    def fake_run(cmd, **kwargs):
        class P:
            returncode = 0
            stdout = fake_heads
            stderr = ""

        return P()

    gec = _load_gec()
    monkeypatch.setattr(gec.subprocess, "run", fake_run)

    cfg = {
        "schemaVersion": "ass-ade.github-evolution-control.v1",
        "global": {"evolutionBranchPrefix": "auto-evolve/", "maxOpenEvolutionPrs": 2},
        "lanes": {"cycle": {"enabled": True, "branchPrefix": "auto-evolve/"}},
    }
    ad = root / ".ass-ade"
    backup = None
    p = ad / "github-evolution-control.json"
    if p.is_file():
        backup = p.read_text(encoding="utf-8")
    try:
        p.write_text(json.dumps(cfg), encoding="utf-8")
        assert gec.cmd_gate("cycle", root) == 0
        assert "proceed=false" in out_file.read_text(encoding="utf-8")
        assert "global_cap" in out_file.read_text(encoding="utf-8")
    finally:
        if backup is not None:
            p.write_text(backup, encoding="utf-8")
        elif p.is_file():
            p.unlink()


def test_count_prefix() -> None:
    gec = _load_gec()
    heads = ["auto-evolve/x", "auto-evolve/quality-a", "main"]
    assert gec._count_prefix(heads, "auto-evolve/quality") == 1
    assert gec._count_prefix(heads, "auto-evolve/") == 2
