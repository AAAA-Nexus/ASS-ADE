# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:321
# Component id: at.source.ass_ade.rank_findings
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
