# Extracted from C:/!ass-ade/tests/test_routing.py:63
# Component id: at.source.ass_ade.test_boundary_fast_standard
from __future__ import annotations

__version__ = "0.1.0"

def test_boundary_fast_standard(self):
    assert tier_for_complexity(0.29) == ModelTier.FAST
    assert tier_for_complexity(0.3) == ModelTier.STANDARD
