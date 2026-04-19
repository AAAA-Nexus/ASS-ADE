# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_default_returns_balanced_tier.py:7
# Component id: at.source.a1_at_functions.test_default_returns_balanced_tier
from __future__ import annotations

__version__ = "0.1.0"

def test_default_returns_balanced_tier(self, monkeypatch):
    # With every catalog provider disabled (incl. pollinations), LSE falls
    # back to the legacy Claude sonnet id.
    lse = self._make(self._no_providers_cfg(monkeypatch))
    decision = lse.select(trs_score=0.75, complexity="medium")
    assert decision.tier == "balanced"
    assert decision.model == "claude-sonnet-4-6"
