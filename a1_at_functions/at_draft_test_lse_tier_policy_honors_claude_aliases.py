# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_tier_policy_honors_claude_aliases.py:7
# Component id: at.source.a1_at_functions.test_lse_tier_policy_honors_claude_aliases
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_tier_policy_honors_claude_aliases(self, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
    from ass_ade.agent.lse import LSEEngine
    # Users configuring with claude tier names should also work
    lse = LSEEngine({
        "tier_policy": {"sonnet": "gemini"},  # sonnet → balanced
    })
    decision = lse.select(trs_score=0.8, complexity="medium")
    assert decision.provider == "gemini"
