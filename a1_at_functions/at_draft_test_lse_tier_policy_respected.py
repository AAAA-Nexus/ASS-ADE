# Extracted from C:/!ass-ade/tests/test_free_providers.py:320
# Component id: at.source.ass_ade.test_lse_tier_policy_respected
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_tier_policy_respected(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
    from ass_ade.agent.lse import LSEEngine
    # Force gemini for balanced, groq for fast
    lse = LSEEngine({
        "tier_policy": {"balanced": "gemini", "fast": "groq"},
    })
    d1 = lse.select(trs_score=0.8, complexity="medium")
    assert d1.provider == "gemini"
    d2 = lse.select(trs_score=0.95, complexity="simple")
    assert d2.provider == "groq"
