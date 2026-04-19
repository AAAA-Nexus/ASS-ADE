# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_selectable_via_tier_policy.py:7
# Component id: at.source.a1_at_functions.test_nexus_selectable_via_tier_policy
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_selectable_via_tier_policy(self, monkeypatch):
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
    from ass_ade.agent.lse import LSEEngine

    lse = LSEEngine({"tier_policy": {"deep": "nexus"}})
    decision = lse.select(trs_score=0.3, complexity="critical")
    assert decision.provider == "nexus"
