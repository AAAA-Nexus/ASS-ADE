# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_run_protocol.py:7
# Component id: at.source.a1_at_functions.run_protocol
from __future__ import annotations

__version__ = "0.1.0"

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
