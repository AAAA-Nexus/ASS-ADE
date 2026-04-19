# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_available_when_key_set.py:7
# Component id: at.source.a1_at_functions.test_nexus_available_when_key_set
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_available_when_key_set(self, monkeypatch):
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
    profile = get_provider("nexus")
    assert profile is not None
    assert profile.is_available() is True
