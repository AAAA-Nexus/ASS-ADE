# Extracted from C:/!ass-ade/tests/test_routing.py:67
# Component id: at.source.ass_ade.test_boundary_standard_deep
from __future__ import annotations

__version__ = "0.1.0"

def test_boundary_standard_deep(self):
    assert tier_for_complexity(0.59) == ModelTier.STANDARD
    assert tier_for_complexity(0.6) == ModelTier.DEEP
