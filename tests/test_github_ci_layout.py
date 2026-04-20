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


def test_github_issue_templates_exist() -> None:
    assert (_REPO / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").is_file()
    assert (_REPO / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").is_file()
    assert (_REPO / ".github" / "ISSUE_TEMPLATE" / "config.yml").is_file()


def test_pull_request_template_exists() -> None:
    assert (_REPO / ".github" / "pull_request_template.md").is_file()


def test_mcp_envelope_spec_exists() -> None:
    p = _REPO / ".ass-ade" / "specs" / "trust-gate-mcp-envelope.spec.md"
    assert p.is_file()
    assert "R1" in p.read_text(encoding="utf-8")


def test_evolution_orchestrate_workflow_exists() -> None:
    wf = _REPO / ".github" / "workflows" / "evolution-orchestrate.yml"
    assert wf.is_file(), f"missing {wf}"
    script = _REPO / "scripts" / "uep_evolution_orchestrator.py"
    assert script.is_file(), f"missing {script}"


def test_github_evolution_control_files_exist() -> None:
    assert (_REPO / "scripts" / "github_evolution_control.py").is_file()
    assert (_REPO / ".ass-ade" / "github-evolution-control.json").is_file()
    wf = _REPO / ".github" / "workflows" / "auto-evolve-cycle.yml"
    text = wf.read_text(encoding="utf-8")
    assert "evolution_gate" in text
    assert "github_evolution_control.py" in text
