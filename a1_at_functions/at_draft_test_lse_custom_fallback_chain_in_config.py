# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_custom_fallback_chain_in_config.py:7
# Component id: at.source.a1_at_functions.test_lse_custom_fallback_chain_in_config
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_custom_fallback_chain_in_config(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
    from ass_ade.agent.lse import LSEEngine
    # User config puts gemini first
    lse = LSEEngine({"provider_fallback_chain": ["gemini", "groq"]})
    decision = lse.select(trs_score=0.8, complexity="medium")
    assert decision.provider == "gemini"
