"""Tests for the free-provider catalog, MultiProvider routing, and LSE integration."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import httpx
import pytest

from ass_ade.agent.providers import (
    ALL_TIERS,
    DEFAULT_FALLBACK_CHAIN,
    FREE_PROVIDERS,
    TIER_ALIASES,
    TIER_BALANCED,
    TIER_DEEP,
    TIER_FAST,
    ProviderProfile,
    detect_available_providers,
    get_provider,
    list_providers,
    provider_for_model,
    resolve_tier,
    select_provider_for_tier,
)


# ─────────────────────────────────────────────────────────────────────────────
# Catalog structure invariants
# ─────────────────────────────────────────────────────────────────────────────


class TestCatalogInvariants:
    def test_catalog_includes_groq_chutes_nexus(self):
        """The three most important providers for a no-budget user must be in the catalog."""
        assert "groq" in FREE_PROVIDERS
        assert "chutes" in FREE_PROVIDERS
        assert "nexus" in FREE_PROVIDERS

    def test_nexus_is_marked_special(self):
        """Nexus uses NexusProvider, not OpenAICompatibleProvider."""
        assert FREE_PROVIDERS["nexus"].special is True

    def test_all_profiles_have_all_three_tiers(self):
        for name, profile in FREE_PROVIDERS.items():
            for tier in ALL_TIERS:
                assert tier in profile.models_by_tier, f"{name} missing {tier} tier"
                assert profile.models_by_tier[tier], f"{name} {tier} is empty"

    def test_all_profiles_have_display_name(self):
        for name, profile in FREE_PROVIDERS.items():
            assert profile.display_name, f"{name} has no display_name"

    def test_local_providers_have_no_api_key_env(self):
        for name, profile in FREE_PROVIDERS.items():
            if profile.local:
                assert profile.api_key_env is None, f"{name} is local but has api_key_env"

    def test_cloud_providers_have_signup_url(self):
        exempt = {"pollinations"}  # no signup needed
        for name, profile in FREE_PROVIDERS.items():
            if not profile.local and name not in exempt:
                assert profile.signup_url, f"{name} is cloud without signup_url"

    def test_fallback_chain_contains_only_known_providers(self):
        known = set(FREE_PROVIDERS.keys())
        for name in DEFAULT_FALLBACK_CHAIN:
            assert name in known, f"fallback chain references unknown provider {name}"

    def test_tier_aliases_include_canonical_and_claude(self):
        assert TIER_ALIASES["haiku"] == TIER_FAST
        assert TIER_ALIASES["sonnet"] == TIER_BALANCED
        assert TIER_ALIASES["opus"] == TIER_DEEP
        assert TIER_ALIASES[TIER_FAST] == TIER_FAST
        assert TIER_ALIASES[TIER_BALANCED] == TIER_BALANCED
        assert TIER_ALIASES[TIER_DEEP] == TIER_DEEP


# ─────────────────────────────────────────────────────────────────────────────
# ProviderProfile behavior
# ─────────────────────────────────────────────────────────────────────────────


class TestProviderProfile:
    def test_resolve_api_key_config_wins(self):
        p = get_provider("groq")
        assert p is not None
        resolved = p.resolve_api_key(config_key="my-config-key")
        assert resolved == "my-config-key"

    def test_resolve_api_key_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "env-key-value")
        p = get_provider("groq")
        assert p.resolve_api_key() == "env-key-value"

    def test_resolve_api_key_returns_none_when_missing(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.resolve_api_key() is None

    def test_local_provider_always_available(self):
        p = get_provider("ollama")
        assert p.local is True
        assert p.is_available() is True  # always true for local

    def test_cloud_provider_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.is_available() is False

    def test_cloud_provider_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        p = get_provider("groq")
        assert p.is_available() is True

    def test_pollinations_available_via_default_key(self):
        p = get_provider("pollinations")
        assert p.is_available() is True

    def test_model_for_tier_honors_override(self):
        p = get_provider("groq")
        override = {"fast": "my-custom-model"}
        assert p.model_for_tier("fast", override=override) == "my-custom-model"
        # Other tiers unaffected
        assert p.model_for_tier("deep", override=override) == p.models_by_tier["deep"]

    def test_model_for_tier_accepts_claude_aliases(self):
        p = get_provider("groq")
        assert p.model_for_tier("haiku") == p.models_by_tier["fast"]
        assert p.model_for_tier("sonnet") == p.models_by_tier["balanced"]
        assert p.model_for_tier("opus") == p.models_by_tier["deep"]


# ─────────────────────────────────────────────────────────────────────────────
# Detection helpers
# ─────────────────────────────────────────────────────────────────────────────


class TestDetection:
    def test_detect_returns_at_least_local_providers(self, monkeypatch):
        # Clear every cloud key
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        available = detect_available_providers({})
        names = {p.name for p in available}
        # Local providers + pollinations (no-key) must be available
        assert "ollama" in names
        assert "pollinations" in names

    def test_detect_skips_disabled_providers(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        available = detect_available_providers({"groq": {"enabled": False}})
        assert "groq" not in {p.name for p in available}

    def test_detect_picks_up_env_key(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        available = detect_available_providers({})
        assert "groq" in {p.name for p in available}

    def test_detect_config_key_overrides_env(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        available = detect_available_providers({"gemini": {"api_key": "config-key"}})
        assert "gemini" in {p.name for p in available}

    def test_provider_for_model_reverse_lookup(self):
        # groq's balanced tier model
        groq_balanced = get_provider("groq").models_by_tier["balanced"]
        assert provider_for_model(groq_balanced) == "groq"

    def test_provider_for_model_unknown_returns_none(self):
        assert provider_for_model("not-a-real-model") is None

    def test_provider_for_model_empty_string(self):
        assert provider_for_model("") is None


# ─────────────────────────────────────────────────────────────────────────────
# Tier → (provider, model) selection
# ─────────────────────────────────────────────────────────────────────────────


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


# ─────────────────────────────────────────────────────────────────────────────
# LSE integrates with the catalog
# ─────────────────────────────────────────────────────────────────────────────


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


# ─────────────────────────────────────────────────────────────────────────────
# MultiProvider routing
# ─────────────────────────────────────────────────────────────────────────────


class TestMultiProvider:
    def _make_provider(self, name: str, fails: bool = False):
        p = MagicMock()
        p.name = name
        if fails:
            p.complete.side_effect = httpx.ConnectError("boom")
        else:
            p.complete.return_value = MagicMock(
                message=MagicMock(content=f"from-{name}", tool_calls=[]),
                usage={"input_tokens": 1, "output_tokens": 1},
            )
        return p

    def test_routes_to_provider_for_known_model(self):
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.types import CompletionRequest, Message
        a = self._make_provider("a")
        b = self._make_provider("b")
        mp = MultiProvider(
            providers={"a": a, "b": b},
            model_to_provider={"model-a": "a", "model-b": "b"},
            fallback_order=["a", "b"],
        )
        req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="model-b")
        mp.complete(req)
        b.complete.assert_called_once()
        a.complete.assert_not_called()
        assert mp.last_provider_name == "b"

    def test_falls_back_on_failure(self):
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.types import CompletionRequest, Message
        failing = self._make_provider("failing", fails=True)
        backup = self._make_provider("backup")
        mp = MultiProvider(
            providers={"failing": failing, "backup": backup},
            model_to_provider={"model-x": "failing"},
            fallback_order=["failing", "backup"],
        )
        req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="model-x")
        resp = mp.complete(req)
        assert mp.last_provider_name == "backup"
        assert resp.message.content == "from-backup"
        failing.complete.assert_called_once()
        backup.complete.assert_called_once()

    def test_unknown_model_uses_fallback_order(self):
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.types import CompletionRequest, Message
        a = self._make_provider("a")
        b = self._make_provider("b")
        mp = MultiProvider(
            providers={"a": a, "b": b},
            model_to_provider={},
            fallback_order=["b", "a"],
        )
        req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="unknown")
        mp.complete(req)
        b.complete.assert_called_once()  # first in fallback

    def test_all_providers_fail_raises(self):
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.types import CompletionRequest, Message
        p1 = self._make_provider("p1", fails=True)
        p2 = self._make_provider("p2", fails=True)
        mp = MultiProvider(
            providers={"p1": p1, "p2": p2},
            model_to_provider={},
            fallback_order=["p1", "p2"],
        )
        req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model=None)
        with pytest.raises(httpx.HTTPError):
            mp.complete(req)

    def test_register_adds_provider_at_runtime(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        mp = MultiProvider(providers={"a": a}, fallback_order=["a"])
        b = self._make_provider("b")
        mp.register("b", b, models=["model-b-1"])
        assert "b" in mp.providers
        assert "b" in mp._fallback_order
        assert mp._model_to_provider["model-b-1"] == "b"

    def test_close_forwards_to_all_underlying(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        b = self._make_provider("b")
        mp = MultiProvider(providers={"a": a, "b": b}, fallback_order=["a", "b"])
        mp.close()
        a.close.assert_called_once()
        b.close.assert_called_once()


# ─────────────────────────────────────────────────────────────────────────────
# build_provider (engine/router.py) builds a MultiProvider from free catalog
# ─────────────────────────────────────────────────────────────────────────────


class TestBuildProviderFromCatalog:
    def test_free_providers_assembled_into_multiprovider(self, monkeypatch):
        # Clear paid keys so we don't hit the legacy path
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        # Clear every cloud catalog key, then set only groq
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")
        monkeypatch.setenv("GEMINI_API_KEY", "sk-gemini")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.router import build_provider

        cfg = AssAdeConfig(profile="local")
        result = build_provider(cfg)
        # With multiple providers, should build a MultiProvider
        assert isinstance(result, MultiProvider)
        # Should contain both groq and gemini
        names = set(result.providers.keys())
        assert "groq" in names
        assert "gemini" in names
        # Pollinations (no-key) should also be present as a fallback
        assert "pollinations" in names

    def test_single_provider_shortcut(self, monkeypatch):
        """When only one provider is available, build_provider returns it directly (no MultiProvider wrapper)."""
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Disable pollinations and ollama to force a single-provider scenario
        from ass_ade.config import AssAdeConfig, ProviderOverride
        from ass_ade.engine.router import build_provider

        cfg = AssAdeConfig(profile="local")
        # Clear available providers except one
        disabled_names = {n for n in FREE_PROVIDERS if n != "groq"}
        for n in disabled_names:
            cfg.providers[n] = ProviderOverride(enabled=False)
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

        result = build_provider(cfg)
        # With exactly one provider, expect a direct OpenAICompatibleProvider
        from ass_ade.engine.provider import OpenAICompatibleProvider
        assert isinstance(result, OpenAICompatibleProvider)

    def test_no_providers_falls_back_to_ollama(self, monkeypatch):
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Disable every catalog provider
        from ass_ade.config import AssAdeConfig, ProviderOverride
        from ass_ade.engine.router import build_provider
        cfg = AssAdeConfig(profile="local")
        for n in FREE_PROVIDERS:
            cfg.providers[n] = ProviderOverride(enabled=False)
        result = build_provider(cfg)
        # Should fall back to Ollama localhost (an OpenAICompatibleProvider)
        from ass_ade.engine.provider import OpenAICompatibleProvider
        assert isinstance(result, OpenAICompatibleProvider)

    def test_explicit_env_override_bypasses_catalog(self, monkeypatch):
        monkeypatch.setenv("ASS_ADE_PROVIDER_URL", "https://custom.example.com/v1")
        monkeypatch.setenv("ASS_ADE_PROVIDER_KEY", "custom-key")
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import OpenAICompatibleProvider
        from ass_ade.engine.router import build_provider

        cfg = AssAdeConfig(profile="local")
        result = build_provider(cfg)
        # Explicit override wins — should be a single OpenAICompatibleProvider
        assert isinstance(result, OpenAICompatibleProvider)


# ─────────────────────────────────────────────────────────────────────────────
# Config extension
# ─────────────────────────────────────────────────────────────────────────────


class TestNexusAsProvider:
    """AAAA-Nexus is selectable like any other provider once the user has a key."""

    def test_nexus_available_when_key_set(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        profile = get_provider("nexus")
        assert profile is not None
        assert profile.is_available() is True

    def test_nexus_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
        profile = get_provider("nexus")
        assert profile.is_available() is False

    def test_nexus_selectable_via_tier_policy(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        from ass_ade.agent.lse import LSEEngine

        lse = LSEEngine({"tier_policy": {"deep": "nexus"}})
        decision = lse.select(trs_score=0.3, complexity="critical")
        assert decision.provider == "nexus"

    def test_build_provider_instantiates_nexus_provider(self, monkeypatch):
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig, ProviderOverride
        from ass_ade.engine.provider import NexusProvider
        from ass_ade.engine.router import build_provider

        # Profile must be non-local for Nexus to wire up
        cfg = AssAdeConfig(profile="hybrid", nexus_api_key="an_test_key")
        # Disable all other catalog providers so Nexus is the only one
        for name in FREE_PROVIDERS:
            if name != "nexus":
                cfg.providers[name] = ProviderOverride(enabled=False)
        provider = build_provider(cfg)
        # With only Nexus enabled, it's returned directly (no MultiProvider wrapper)
        assert isinstance(provider, NexusProvider)

    def test_nexus_is_in_default_fallback_chain(self):
        assert "nexus" in DEFAULT_FALLBACK_CHAIN

    def test_nexus_skipped_in_local_profile(self, monkeypatch):
        """Nexus is a metered paid-ish provider; local profile should skip it."""
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.router import build_provider

        cfg = AssAdeConfig(profile="local", nexus_api_key="an_test_key")
        provider = build_provider(cfg)
        # Nexus must not be in the provider map when profile is local
        if hasattr(provider, "providers"):
            assert "nexus" not in provider.providers


class TestChutesProvider:
    """Chutes.ai — free DeepSeek V3/R1 via Bittensor subnet."""

    def test_chutes_in_catalog(self):
        assert "chutes" in FREE_PROVIDERS

    def test_chutes_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
        profile = get_provider("chutes")
        assert profile.is_available() is True

    def test_chutes_serves_deepseek_models(self):
        profile = get_provider("chutes")
        assert "deepseek" in profile.models_by_tier["balanced"].lower()
        assert "deepseek" in profile.models_by_tier["deep"].lower()

    def test_chutes_selectable_via_tier_policy(self, monkeypatch):
        monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
        from ass_ade.agent.lse import LSEEngine

        lse = LSEEngine({"tier_policy": {"deep": "chutes"}})
        decision = lse.select(trs_score=0.3, complexity="critical")
        assert decision.provider == "chutes"
        assert "deepseek" in decision.model.lower()


class TestConfigProviderFields:
    def test_default_config_has_new_fields(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig()
        assert cfg.lse_enabled is True
        assert cfg.tier_policy == {}
        assert cfg.provider_fallback_chain == []
        assert cfg.providers == {}

    def test_provider_override_parses_from_json(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig.model_validate({
            "profile": "local",
            "providers": {
                "groq": {"enabled": True, "api_key": "sk-test"},
                "gemini": {"enabled": False},
            },
            "tier_policy": {"balanced": "groq"},
            "provider_fallback_chain": ["groq", "gemini", "ollama"],
        })
        assert cfg.providers["groq"].api_key == "sk-test"
        assert cfg.providers["gemini"].enabled is False
        assert cfg.tier_policy == {"balanced": "groq"}
        assert cfg.provider_fallback_chain == ["groq", "gemini", "ollama"]

    def test_write_config_does_not_persist_api_keys(self, tmp_path):
        from ass_ade.config import AssAdeConfig, ProviderOverride, write_default_config
        cfg = AssAdeConfig(
            profile="local",
            providers={"groq": ProviderOverride(enabled=True, api_key="sk-secret")},
        )
        path = tmp_path / "config.json"
        write_default_config(path, config=cfg, overwrite=True)
        written = path.read_text(encoding="utf-8")
        assert "sk-secret" not in written
        assert "nexus_api_key" not in written

    def test_env_hydration_populates_os_environ(self, tmp_path, monkeypatch):
        from ass_ade.config import load_config
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        # Write a .env at project root
        (tmp_path / ".env").write_text("GROQ_API_KEY=from-env-file\n")
        (tmp_path / ".ass-ade").mkdir()
        config_path = tmp_path / ".ass-ade" / "config.json"
        load_config(config_path)
        assert os.getenv("GROQ_API_KEY") == "from-env-file"

    def test_env_hydration_does_not_override_process_env(self, tmp_path, monkeypatch):
        from ass_ade.config import load_config
        monkeypatch.setenv("GROQ_API_KEY", "from-process")
        (tmp_path / ".env").write_text("GROQ_API_KEY=from-file\n")
        (tmp_path / ".ass-ade").mkdir()
        load_config(tmp_path / ".ass-ade" / "config.json")
        # Process env wins
        assert os.getenv("GROQ_API_KEY") == "from-process"
