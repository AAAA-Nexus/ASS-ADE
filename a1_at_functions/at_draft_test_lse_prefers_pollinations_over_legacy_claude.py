# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_prefers_pollinations_over_legacy_claude.py:7
# Component id: at.source.a1_at_functions.test_lse_prefers_pollinations_over_legacy_claude
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_prefers_pollinations_over_legacy_claude(self, monkeypatch):
    """Without any free provider keys, LSE prefers the no-key pollinations
    endpoint over the legacy Claude id (so users without an Anthropic key
    don't hit 401s)."""
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    # Disable every catalog provider EXCEPT pollinations
    disabled = {
        name: {"enabled": False}
        for name in FREE_PROVIDERS
        if name != "pollinations"
    }
    from ass_ade.agent.lse import LSEEngine

    lse = LSEEngine({"providers": disabled})
    decision = lse.select(trs_score=0.8, complexity="medium")
    assert decision.provider == "pollinations"
