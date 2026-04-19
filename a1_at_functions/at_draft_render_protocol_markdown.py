# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_render_protocol_markdown.py:7
# Component id: at.source.a1_at_functions.render_protocol_markdown
from __future__ import annotations

__version__ = "0.1.0"

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
