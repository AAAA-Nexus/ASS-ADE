# Extracted from C:/!ass-ade/tests/test_free_providers.py:573
# Component id: at.source.ass_ade.test_nexus_unavailable_without_key
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_unavailable_without_key(self, monkeypatch):
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    profile = get_provider("nexus")
    assert profile.is_available() is False
