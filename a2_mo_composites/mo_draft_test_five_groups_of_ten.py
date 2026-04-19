# Extracted from C:/!ass-ade/tests/test_engine_integration.py:42
# Component id: mo.source.ass_ade.test_five_groups_of_ten
from __future__ import annotations

__version__ = "0.1.0"

def test_five_groups_of_ten(self) -> None:
    from collections import Counter
    groups = Counter(q["group"] for q in AUDIT_QUESTIONS)
    assert set(groups.keys()) == {"foundational", "operational", "autonomous", "meta_cognition", "hyperagent"}
    assert all(v == 10 for v in groups.values())
