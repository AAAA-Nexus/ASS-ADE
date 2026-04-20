from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ass_ade.config import AssAdeConfig
from ass_ade.local.planner import draft_plan
from ass_ade.local.repo import RepoSummary, summarize_repo
from ass_ade.system import ToolStatus, collect_tool_status


class ProtocolAuditCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class ProtocolAssessment(BaseModel):
    root: str
    total_files: int
    total_dirs: int
    top_level_entries: list[str]
    file_types: dict[str, int]
    toolchain: list[dict[str, str | bool | None]]
    profile: str
    local_mode_default: bool


class ProtocolReport(BaseModel):
    protocol_name: str = "ASS-ADE Public Enhancement Cycle"
    goal: str
    assessment: ProtocolAssessment
    design_steps: list[str]
    audit: list[ProtocolAuditCheck]
    recommendations: list[str]
    summary: str


def _tool_status_payload(items: list[ToolStatus]) -> list[dict[str, str | bool | None]]:
    return [
        {
            "name": item.name,
            "available": item.available,
            "version": item.version,
            "error": item.error,
        }
        for item in items
    ]


def build_assessment(root: Path, settings: AssAdeConfig) -> ProtocolAssessment:
    repo_summary: RepoSummary = summarize_repo(root)
    toolchain = collect_tool_status()

    return ProtocolAssessment(
        root=str(repo_summary.root),
        total_files=repo_summary.total_files,
        total_dirs=repo_summary.total_dirs,
        top_level_entries=repo_summary.top_level_entries,
        file_types=repo_summary.file_types,
        toolchain=_tool_status_payload(toolchain),
        profile=settings.profile,
        local_mode_default=settings.profile == "local",
    )


def build_audit(root: Path, settings: AssAdeConfig) -> list[ProtocolAuditCheck]:
    checks: list[ProtocolAuditCheck] = []

    required_files = [
        root / "README.md",
        root / "docs" / "architecture.md",
        root / "docs" / "dev-stack.md",
        root / ".github" / "copilot-instructions.md",
        root / "pyproject.toml",
        root / "src" / "ass_ade" / "cli.py",
        root / "src" / "ass_ade" / "nexus" / "models.py",
        root / "src" / "ass_ade" / "local" / "repo.py",
        root / "tests" / "test_cli.py",
    ]
    checks.append(
        ProtocolAuditCheck(
            name="Public shell scaffold present",
            passed=all(path.exists() for path in required_files),
            detail="Checks that docs, package config, CLI, typed contracts, local utility, and tests exist.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Local mode is the default",
            passed=settings.profile == "local",
            detail=f"Current profile is '{settings.profile}'. Public-safe default should remain local.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Remote contract boundary preserved",
            passed=(root / "src" / "ass_ade" / "nexus" / "models.py").exists(),
            detail="Typed public-contract models should exist instead of raw backend logic in the repo.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Standalone local value exists",
            passed=(root / "src" / "ass_ade" / "local" / "repo.py").exists(),
            detail="The repo should ship at least one genuinely useful local capability with no premium dependency.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Protocol docs are public-safe",
            passed=(root / "docs" / "protocol.md").exists(),
            detail="The sanitized protocol should be documented without embedding private backend internals.",
        )
    )

    return checks


def build_recommendations(audit: list[ProtocolAuditCheck], goal: str) -> list[str]:
    recommendations: list[str] = []

    if not any(check.name == "Protocol docs are public-safe" and check.passed for check in audit):
        recommendations.append(
            "Document the public-safe protocol cycle so contributors know what ASS-ADE may and may not inherit from private backend patterns."
        )

    if not any(check.name == "Standalone local value exists" and check.passed for check in audit):
        recommendations.append(
            "Add another local-only capability so the public repo keeps earning attention even without remote endpoints."
        )

    for check in audit:
        if check.name == "Local mode is the default" and not check.passed:
            recommendations.append("Reset profile to 'local' in config: ass-ade config set profile local")
        elif check.name == "Public shell scaffold present" and not check.passed:
            recommendations.append("Run 'ass-ade init' to create the required scaffold structure")
        elif check.name == "Remote contract boundary preserved" and not check.passed:
            recommendations.append("Remove any private backend references from public-facing modules")

    recommendations.append(f"Use the next enhancement cycle to target: {goal}")
    recommendations.append(
        "Prefer typed public contracts, degraded local fallbacks, and explicit remote opt-in over reproducing backend logic locally."
    )
    return recommendations


def run_protocol(goal: str, root: Path, settings: AssAdeConfig) -> ProtocolReport:
    assessment = build_assessment(root, settings)
    audit = build_audit(root, settings)
    design_steps = draft_plan(goal, max_steps=6)
    recommendations = build_recommendations(audit, goal)
    passed = sum(1 for item in audit if item.passed)

    summary = (
        f"Completed a public-safe enhancement cycle for '{goal}'. "
        f"Audit passed {passed}/{len(audit)} checks in {settings.profile} profile."
    )

    return ProtocolReport(
        goal=goal,
        assessment=assessment,
        design_steps=design_steps,
        audit=audit,
        recommendations=recommendations,
        summary=summary,
    )


def render_protocol_markdown(report: ProtocolReport) -> str:
    lines = [
        f"# {report.protocol_name}",
        "",
        f"Goal: {report.goal}",
        "",
        "## Assessment",
        "",
        f"- Root: {report.assessment.root}",
        f"- Profile: {report.assessment.profile}",
        f"- Files: {report.assessment.total_files}",
        f"- Directories: {report.assessment.total_dirs}",
        f"- Top-level entries: {', '.join(report.assessment.top_level_entries[:12]) or 'none'}",
        "",
        "## Design",
        "",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(report.design_steps, start=1))
    lines.extend(["", "## Audit", ""])
    lines.extend(
        f"- [{'PASS' if check.passed else 'FAIL'}] {check.name}: {check.detail}" for check in report.audit
    )
    lines.extend(["", "## Recommendations", ""])
    lines.extend(f"- {item}" for item in report.recommendations)
    lines.extend(["", "## Summary", "", report.summary])
    return "\n".join(lines)
