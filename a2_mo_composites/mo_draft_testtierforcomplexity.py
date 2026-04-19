# Extracted from C:/!ass-ade/tests/test_routing.py:53
# Component id: mo.source.ass_ade.testtierforcomplexity
from __future__ import annotations

__version__ = "0.1.0"

class TestTierForComplexity:
    def test_fast(self):
        assert tier_for_complexity(0.1) == ModelTier.FAST

    def test_standard(self):
        assert tier_for_complexity(0.4) == ModelTier.STANDARD

    def test_deep(self):
        assert tier_for_complexity(0.8) == ModelTier.DEEP

    def test_boundary_fast_standard(self):
        assert tier_for_complexity(0.29) == ModelTier.FAST
        assert tier_for_complexity(0.3) == ModelTier.STANDARD

    def test_boundary_standard_deep(self):
        assert tier_for_complexity(0.59) == ModelTier.STANDARD
        assert tier_for_complexity(0.6) == ModelTier.DEEP
