# Extracted from C:/!ass-ade/tests/test_free_providers.py:243
# Component id: at.source.ass_ade.test_returns_none_when_no_providers
from __future__ import annotations

__version__ = "0.1.0"

def test_returns_none_when_no_providers(self, monkeypatch):
    # Clear every key AND disable all providers
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    disabled = {name: {"enabled": False} for name in FREE_PROVIDERS}
    match = select_provider_for_tier("balanced", config_providers=disabled)
    assert match is None
