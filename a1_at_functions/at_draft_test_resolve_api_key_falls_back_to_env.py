# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_resolve_api_key_falls_back_to_env.py:7
# Component id: at.source.a1_at_functions.test_resolve_api_key_falls_back_to_env
from __future__ import annotations

__version__ = "0.1.0"

def test_resolve_api_key_falls_back_to_env(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "env-key-value")
    p = get_provider("groq")
    assert p.resolve_api_key() == "env-key-value"
