# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_returns_at_least_local_providers.py:7
# Component id: at.source.a1_at_functions.test_detect_returns_at_least_local_providers
from __future__ import annotations

__version__ = "0.1.0"

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
