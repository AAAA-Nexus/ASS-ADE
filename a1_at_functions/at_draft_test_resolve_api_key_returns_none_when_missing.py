# Extracted from C:/!ass-ade/tests/test_free_providers.py:96
# Component id: at.source.ass_ade.test_resolve_api_key_returns_none_when_missing
from __future__ import annotations

__version__ = "0.1.0"

def test_resolve_api_key_returns_none_when_missing(self, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    p = get_provider("groq")
    assert p.resolve_api_key() is None
