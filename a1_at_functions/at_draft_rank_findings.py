# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_rank_findings.py:7
# Component id: at.source.a1_at_functions.rank_findings
from __future__ import annotations

__version__ = "0.1.0"

def rank_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    impact_order = {"high": 0, "medium": 1, "low": 2}
    effort_order = {"low": 0, "medium": 1, "high": 2}
    ranked = sorted(
        findings,
        key=lambda f: (impact_order.get(f.get("impact", "low"), 2), effort_order.get(f.get("effort", "medium"), 1)),
    )
    for i, finding in enumerate(ranked, start=1):
        finding["id"] = i
    return ranked
