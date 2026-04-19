# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testauditquestions.py:11
# Component id: at.source.a2_mo_composites.test_all_texts_unique
from __future__ import annotations

__version__ = "0.1.0"

def test_all_texts_unique(self) -> None:
    texts = [q["text"] for q in AUDIT_QUESTIONS]
    assert len(set(texts)) == 50, "All 50 audit questions must have distinct text"
