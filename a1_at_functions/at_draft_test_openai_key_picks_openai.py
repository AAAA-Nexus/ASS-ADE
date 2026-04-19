# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_openai_key_picks_openai.py:7
# Component id: at.source.a1_at_functions.test_openai_key_picks_openai
from __future__ import annotations

__version__ = "0.1.0"

def test_openai_key_picks_openai(self, monkeypatch):
    self._clear_provider_env()
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    from ass_ade.config import AssAdeConfig
    from ass_ade.engine.provider import MultiProvider

    cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
    provider = build_provider(cfg)
    # With catalog disabled and only OPENAI_API_KEY set, should get a single provider
    assert isinstance(provider, OpenAICompatibleProvider)
