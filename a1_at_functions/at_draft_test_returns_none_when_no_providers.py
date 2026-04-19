# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_returns_none_when_no_providers.py:7
# Component id: at.source.a1_at_functions.test_returns_none_when_no_providers
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
