# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhancer.py:173
# Component id: at.source.ass_ade.test_rank_findings_order
__version__ = "0.1.0"

def test_rank_findings_order() -> None:
    findings: list[dict[str, Any]] = [
        {"id": 1, "impact": "low", "effort": "low", "category": "a"},
        {"id": 2, "impact": "high", "effort": "medium", "category": "b"},
        {"id": 3, "impact": "medium", "effort": "low", "category": "c"},
    ]

    ranked = rank_findings(findings)

    assert ranked[0]["impact"] == "high"
