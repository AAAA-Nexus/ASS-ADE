"""Sanity: expected GitHub automation files stay present (MAP=TERRAIN lane wiring)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def test_pr_labeled_workflow_exists() -> None:
    path = _REPO / ".github" / "workflows" / "pr-labeled-ass-ade.yml"
    assert path.is_file(), f"missing {path}"


def test_atomadic_dev_harness_script_exists() -> None:
    path = _REPO / "scripts" / "atomadic_dev_harness.py"
    assert path.is_file(), f"missing {path}"


def test_contributing_documents_label_lanes() -> None:
    text = (_REPO / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "ass-ade-blueprint" in text
    assert "ass-ade-feature" in text


def test_evolution_prune_and_gate_workflows_exist() -> None:
    prune = _REPO / ".github" / "workflows" / "evolution-branch-prune.yml"
    gate = _REPO / ".github" / "workflows" / "evolution-pr-gate.yml"
    assert prune.is_file(), f"missing {prune}"
    assert gate.is_file(), f"missing {gate}"


def test_prune_evolution_branches_script_help() -> None:
    script = _REPO / "scripts" / "prune_evolution_branches.py"
    assert script.is_file()
    out = subprocess.check_output(
        [sys.executable, str(script), "--help"],
        text=True,
    )
    assert "--stale-days" in out
    assert "--dry-run" in out
