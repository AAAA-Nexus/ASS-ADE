# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_boundary_standard_deep.py:7
# Component id: at.source.a1_at_functions.test_boundary_standard_deep
from __future__ import annotations

__version__ = "0.1.0"

def test_boundary_standard_deep(self):
    assert tier_for_complexity(0.59) == ModelTier.STANDARD
    assert tier_for_complexity(0.6) == ModelTier.DEEP
