# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_formal_verification.py:7
# Component id: at.source.a1_at_functions.test_formal_verification
from __future__ import annotations

__version__ = "0.1.0"

def test_formal_verification(self):
    c = classify_complexity(
        "Write a formal proof that this invariant holds across all states"
    )
    assert c >= 0.2  # formal keywords detected
