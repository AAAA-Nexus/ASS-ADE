# Extracted from C:/!ass-ade/tests/test_phase_engines.py:32
# Component id: mo.source.ass_ade.test_default_returns_balanced_tier
from __future__ import annotations

__version__ = "0.1.0"

def test_default_returns_balanced_tier(self, monkeypatch):
    # With every catalog provider disabled (incl. pollinations), LSE falls
    # back to the legacy Claude sonnet id.
    lse = self._make(self._no_providers_cfg(monkeypatch))
    decision = lse.select(trs_score=0.75, complexity="medium")
    assert decision.tier == "balanced"
    assert decision.model == "claude-sonnet-4-6"
