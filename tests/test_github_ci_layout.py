"""Sanity: expected GitHub automation files stay present (MAP=TERRAIN lane wiring)."""

from __future__ import annotations

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
