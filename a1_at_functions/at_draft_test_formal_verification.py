# Extracted from C:/!ass-ade/tests/test_routing.py:31
# Component id: at.source.ass_ade.test_formal_verification
from __future__ import annotations

__version__ = "0.1.0"

def test_formal_verification(self):
    c = classify_complexity(
        "Write a formal proof that this invariant holds across all states"
    )
    assert c >= 0.2  # formal keywords detected
