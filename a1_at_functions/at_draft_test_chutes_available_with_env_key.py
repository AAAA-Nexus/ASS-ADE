# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_chutes_available_with_env_key.py:7
# Component id: at.source.a1_at_functions.test_chutes_available_with_env_key
from __future__ import annotations

__version__ = "0.1.0"

def test_chutes_available_with_env_key(self, monkeypatch):
    monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
    profile = get_provider("chutes")
    assert profile.is_available() is True
