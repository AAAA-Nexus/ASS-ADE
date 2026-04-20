"""Tests for governance evolution orchestration handoff (offline heuristics)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def test_build_research_pack_shapes() -> None:
    from ass_ade.local.uep_evolution_orchestrate import build_research_pack

    root = _REPO
    pack = build_research_pack(
        task="Harden MCP server integration and pytest coverage",
        root=root,
        repo="AAAA-Nexus/ASS-ADE",
    )
    assert pack["schemaVersion"] == "atomadic.context-pack.v1"
    hops = pack["webResearch"]["hops"]
    assert len(hops) >= 4
    assert all("queries" in h for h in hops)
    assert any(h.get("id") == "H4-formal-codex-boundary" for h in hops)


def test_build_research_pack_with_formal_codex_context_has_extensions() -> None:
    from ass_ade.local.uep_evolution_orchestrate import build_research_pack

    bridge = {
        "sourcePath": "/tmp/codex.json",
        "documentId": "DOC-1",
        "title": "T",
        "version": "v1",
        "epistemicStatusProse": "",
        "epistemicStatusCodes": [{"code": "[L]", "meaning": "Lean", "notes": "n"}],
        "lean4Summary": None,
        "operatorNote": "x",
    }
    pack = build_research_pack(
        task="task",
        root=_REPO,
        repo="AAAA-Nexus/ASS-ADE",
        formal_codex_context=bridge,
    )
    assert pack["extensions"]["formalCodexContext"]["documentId"] == "DOC-1"
    assert "governancePhases" in pack


def test_load_formal_codex_context_minimal(tmp_path: Path) -> None:
    from ass_ade.local.uep_evolution_orchestrate import load_formal_codex_context

    p = tmp_path / "c.json"
    p.write_text(
        '{"document_id":"X","epistemic_status_codes":[{"code":"[S]","meaning":"Spec","notes":""}],'
        '"lean4_verification":{"status":"ok","as_of":"d","total_theorems":1,"total_sorry":0}}',
        encoding="utf-8",
    )
    b = load_formal_codex_context(p)
    assert b is not None
    assert b["documentId"] == "X"
    assert b["epistemicStatusCodes"][0]["code"] == "[S]"
    assert b["lean4Summary"]["totalTheorems"] == 1


def test_discover_formal_codex_json_path_explicit(tmp_path: Path) -> None:
    from ass_ade.local.uep_evolution_orchestrate import discover_formal_codex_json_path

    p = tmp_path / "a.json"
    p.write_text("{}", encoding="utf-8")
    assert discover_formal_codex_json_path(p) == p
    assert discover_formal_codex_json_path(tmp_path / "missing.json") is None


def test_render_evolution_audit_contains_trust_gate_line() -> None:
    from ass_ade.local.uep_evolution_orchestrate import render_evolution_audit_checklist

    md = render_evolution_audit_checklist(task="t", formal_codex_context=None)
    assert "Trust-before-memory" in md
    assert "trust_gate" in md


def test_discover_tech_doc_paths_finds_readme(tmp_path: Path) -> None:
    from ass_ade.local.uep_evolution_orchestrate import discover_tech_doc_paths

    (tmp_path / "README.md").write_text("# demo\nmcp nexus\n", encoding="utf-8")
    found = discover_tech_doc_paths(tmp_path, "document MCP nexus flows", limit=5)
    assert "README.md" in found


def test_uep_evolution_orchestrator_help() -> None:
    script = _REPO / "scripts" / "uep_evolution_orchestrator.py"
    out = subprocess.check_output([sys.executable, str(script), "--help"], text=True)
    assert "--task-file" in out
    assert "--formal-codex-json" in out
