# Extracted from C:/!ass-ade/tests/test_free_providers.py:636
# Component id: at.source.ass_ade.test_chutes_available_with_env_key
from __future__ import annotations

__version__ = "0.1.0"

def test_chutes_available_with_env_key(self, monkeypatch):
    monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
    profile = get_provider("chutes")
    assert profile.is_available() is True
