# Extracted from C:/!ass-ade/tests/test_free_providers.py:33
# Component id: qk.source.ass_ade.testcataloginvariants
from __future__ import annotations

__version__ = "0.1.0"

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
