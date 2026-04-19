# Extracted from C:/!ass-ade/tests/test_free_providers.py:140
# Component id: at.source.ass_ade.test_detect_returns_at_least_local_providers
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
