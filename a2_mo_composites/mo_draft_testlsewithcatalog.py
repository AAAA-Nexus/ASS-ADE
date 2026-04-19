# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlsewithcatalog.py:7
# Component id: mo.source.a2_mo_composites.testlsewithcatalog
from __future__ import annotations

__version__ = "0.1.0"

class TestLSEWithCatalog:
    def test_lse_uses_free_provider_when_key_present(self, monkeypatch):
        # Clear all keys, then give only groq
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")

        from ass_ade.agent.lse import LSEEngine
        lse = LSEEngine({})
        decision = lse.select(trs_score=0.8, complexity="medium")
        # Should pick the Groq balanced model
        assert decision.provider == "groq"
        expected_model = get_provider("groq").models_by_tier["balanced"]
        assert decision.model == expected_model

    def test_lse_falls_back_to_pollinations_when_catalog_disabled(self, monkeypatch):
        """Without any free provider keys AND pollinations explicitly disabled,
        LSE falls back to legacy Claude sonnet."""
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Disable EVERY catalog entry (including pollinations, the no-key default)
        disabled_cfg = {name: {"enabled": False} for name in FREE_PROVIDERS}
        from ass_ade.agent.lse import LSEEngine, _LEGACY_TIER_TO_MODEL

        lse = LSEEngine({"providers": disabled_cfg})
        decision = lse.select(trs_score=0.8, complexity="medium")
        # With pollinations disabled, the only remaining fallback is the legacy Claude id
        assert decision.provider is None
        assert decision.model == _LEGACY_TIER_TO_MODEL["balanced"]

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

    def test_lse_tier_policy_honors_claude_aliases(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        from ass_ade.agent.lse import LSEEngine
        # Users configuring with claude tier names should also work
        lse = LSEEngine({
            "tier_policy": {"sonnet": "gemini"},  # sonnet → balanced
        })
        decision = lse.select(trs_score=0.8, complexity="medium")
        assert decision.provider == "gemini"

    def test_lse_user_override_bypasses_catalog(self):
        from ass_ade.agent.lse import LSEEngine
        lse = LSEEngine({})
        decision = lse.select(
            trs_score=0.8, complexity="medium", user_model_override="my-fixed-model",
        )
        assert decision.model == "my-fixed-model"
        assert decision.provider is None
        assert decision.reason == "user_override"

    def test_lse_report_includes_provider_distribution(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        from ass_ade.agent.lse import LSEEngine
        lse = LSEEngine({})
        lse.select(trs_score=0.9, complexity="medium")
        lse.select(trs_score=0.3, complexity="complex")
        rep = lse.report()
        assert "provider_distribution" in rep
        assert "last_provider" in rep

    def test_lse_custom_fallback_chain_in_config(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        from ass_ade.agent.lse import LSEEngine
        # User config puts gemini first
        lse = LSEEngine({"provider_fallback_chain": ["gemini", "groq"]})
        decision = lse.select(trs_score=0.8, complexity="medium")
        assert decision.provider == "gemini"
