# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testauditquestions.py:25
# Component id: at.source.a2_mo_composites.test_all_have_required_keys
from __future__ import annotations

__version__ = "0.1.0"

def test_all_have_required_keys(self) -> None:
    for q in AUDIT_QUESTIONS:
        assert "id" in q and "group" in q and "text" in q
        assert isinstance(q["text"], str) and q["text"]
