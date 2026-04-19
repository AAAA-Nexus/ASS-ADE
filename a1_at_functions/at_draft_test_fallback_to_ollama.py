# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fallback_to_ollama.py:7
# Component id: at.source.a1_at_functions.test_fallback_to_ollama
from __future__ import annotations

__version__ = "0.1.0"

def test_fallback_to_ollama(self, monkeypatch):
    """With no keys and all catalog providers disabled, falls back to Ollama."""
    self._clear_provider_env()

    from ass_ade.config import AssAdeConfig

    cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
    provider = build_provider(cfg)
    assert isinstance(provider, OpenAICompatibleProvider)
