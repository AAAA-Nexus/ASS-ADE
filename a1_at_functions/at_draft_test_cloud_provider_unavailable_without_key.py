# Extracted from C:/!ass-ade/tests/test_free_providers.py:106
# Component id: at.source.ass_ade.test_cloud_provider_unavailable_without_key
from __future__ import annotations

__version__ = "0.1.0"

def test_cloud_provider_unavailable_without_key(self, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    p = get_provider("groq")
    assert p.is_available() is False
