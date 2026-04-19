# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_added_to_multiprovider_when_catalog_keys_present.py:7
# Component id: at.source.a1_at_functions.test_nexus_added_to_multiprovider_when_catalog_keys_present
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_added_to_multiprovider_when_catalog_keys_present(self, monkeypatch):
    """Premium profile + catalog keys → MultiProvider containing nexus + free providers."""
    self._clear_provider_env()
    monkeypatch.setenv("GROQ_API_KEY", "sk-groq")
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

    from ass_ade.config import AssAdeConfig
    from ass_ade.engine.provider import MultiProvider

    cfg = AssAdeConfig(
        profile="premium",
        nexus_api_key="an_test_key",
        nexus_base_url="https://atomadic.tech",
    )
    provider = build_provider(cfg)
    assert isinstance(provider, MultiProvider)
    assert "nexus" in provider.providers
    assert "groq" in provider.providers
