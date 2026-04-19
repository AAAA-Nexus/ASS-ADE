# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_unavailable_without_key.py:7
# Component id: at.source.a1_at_functions.test_nexus_unavailable_without_key
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_unavailable_without_key(self, monkeypatch):
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    profile = get_provider("nexus")
    assert profile.is_available() is False
