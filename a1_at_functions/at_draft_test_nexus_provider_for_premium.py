# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_provider_for_premium.py:7
# Component id: at.source.a1_at_functions.test_nexus_provider_for_premium
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_provider_for_premium(self, monkeypatch):
    self._clear_provider_env()
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

    from ass_ade.config import AssAdeConfig

    cfg = self._disable_all_catalog(
        AssAdeConfig(
            profile="premium",
            nexus_api_key="an_test_key",
            nexus_base_url="https://atomadic.tech",
        ),
        keep=("nexus",),  # leave Nexus enabled
    )
    provider = build_provider(cfg)
    # Only Nexus enabled → single return
    assert isinstance(provider, NexusProvider)
