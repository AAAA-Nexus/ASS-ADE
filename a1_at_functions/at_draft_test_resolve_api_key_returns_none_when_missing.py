# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_resolve_api_key_returns_none_when_missing.py:7
# Component id: at.source.a1_at_functions.test_resolve_api_key_returns_none_when_missing
from __future__ import annotations

__version__ = "0.1.0"

def test_resolve_api_key_returns_none_when_missing(self, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    p = get_provider("groq")
    assert p.resolve_api_key() is None
