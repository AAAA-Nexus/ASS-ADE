# Extracted from C:/!ass-ade/tests/test_enhancer.py:185
# Component id: at.source.ass_ade.test_rank_findings_reassigns_ids
from __future__ import annotations

__version__ = "0.1.0"

def test_rank_findings_reassigns_ids() -> None:
    findings: list[dict[str, Any]] = [
        {"id": 10, "impact": "low", "effort": "low", "category": "a"},
        {"id": 5, "impact": "medium", "effort": "low", "category": "b"},
        {"id": 7, "impact": "high", "effort": "low", "category": "c"},
    ]

    ranked = rank_findings(findings)

    ids = [f["id"] for f in ranked]
    assert ids == [1, 2, 3]
