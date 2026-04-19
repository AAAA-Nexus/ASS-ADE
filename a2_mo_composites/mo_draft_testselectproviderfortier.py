# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testselectproviderfortier.py:7
# Component id: mo.source.a2_mo_composites.testselectproviderfortier
from __future__ import annotations

__version__ = "0.1.0"

class TestSelectProviderForTier:
    def test_selects_first_available_in_chain(self, monkeypatch):
        # Clear all cloud keys
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Give only groq a key
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        match = select_provider_for_tier("balanced")
        assert match is not None
        profile, model = match
        assert profile.name == "groq"
        assert model == profile.models_by_tier["balanced"]

    def test_policy_overrides_chain_order(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        # Policy forces gemini for balanced
        match = select_provider_for_tier(
            "balanced",
            tier_policy={"balanced": "gemini"},
        )
        assert match is not None
        profile, _ = match
        assert profile.name == "gemini"

    def test_falls_through_when_policy_unavailable(self, monkeypatch):
        # Policy says gemini, but gemini has no key — fall through to next chain provider
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        match = select_provider_for_tier(
            "balanced",
            tier_policy={"balanced": "gemini"},
        )
        assert match is not None
        profile, _ = match
        # Falls through to groq (only one with a key)
        assert profile.name == "groq"

    def test_custom_fallback_chain_respected(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
        # Custom chain puts gemini first
        match = select_provider_for_tier(
            "balanced",
            fallback_chain=["gemini", "groq"],
        )
        assert match is not None
        profile, _ = match
        assert profile.name == "gemini"

    def test_claude_tier_alias_works(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        match = select_provider_for_tier("haiku")  # alias for "fast"
        assert match is not None
        profile, model = match
        assert model == profile.models_by_tier["fast"]

    def test_returns_none_when_no_providers(self, monkeypatch):
        # Clear every key AND disable all providers
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        disabled = {name: {"enabled": False} for name in FREE_PROVIDERS}
        match = select_provider_for_tier("balanced", config_providers=disabled)
        assert match is None

    def test_config_override_model_honored(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        match = select_provider_for_tier(
            "balanced",
            config_providers={"groq": {"models_by_tier": {"balanced": "my-tuned-model"}}},
        )
        assert match is not None
        profile, model = match
        assert profile.name == "groq"
        assert model == "my-tuned-model"
