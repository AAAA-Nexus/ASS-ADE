# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testauditquestions.py:19
# Component id: at.source.a2_mo_composites.test_five_groups_of_ten
from __future__ import annotations

__version__ = "0.1.0"

def test_five_groups_of_ten(self) -> None:
    from collections import Counter
    groups = Counter(q["group"] for q in AUDIT_QUESTIONS)
    assert set(groups.keys()) == {"foundational", "operational", "autonomous", "meta_cognition", "hyperagent"}
    assert all(v == 10 for v in groups.values())
