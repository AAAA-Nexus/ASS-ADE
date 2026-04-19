# Extracted from C:/!ass-ade/tests/test_free_providers.py:353
# Component id: at.source.ass_ade.test_lse_report_includes_provider_distribution
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_report_includes_provider_distribution(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    from ass_ade.agent.lse import LSEEngine
    lse = LSEEngine({})
    lse.select(trs_score=0.9, complexity="medium")
    lse.select(trs_score=0.3, complexity="complex")
    rep = lse.report()
    assert "provider_distribution" in rep
    assert "last_provider" in rep
