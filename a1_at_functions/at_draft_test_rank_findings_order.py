# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rank_findings_order.py:7
# Component id: at.source.a1_at_functions.test_rank_findings_order
from __future__ import annotations

__version__ = "0.1.0"

def test_rank_findings_order() -> None:
    findings: list[dict[str, Any]] = [
        {"id": 1, "impact": "low", "effort": "low", "category": "a"},
        {"id": 2, "impact": "high", "effort": "medium", "category": "b"},
        {"id": 3, "impact": "medium", "effort": "low", "category": "c"},
    ]

    ranked = rank_findings(findings)

    assert ranked[0]["impact"] == "high"
