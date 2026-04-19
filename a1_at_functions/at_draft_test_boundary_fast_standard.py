# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_boundary_fast_standard.py:7
# Component id: at.source.a1_at_functions.test_boundary_fast_standard
from __future__ import annotations

__version__ = "0.1.0"

def test_boundary_fast_standard(self):
    assert tier_for_complexity(0.29) == ModelTier.FAST
    assert tier_for_complexity(0.3) == ModelTier.STANDARD
