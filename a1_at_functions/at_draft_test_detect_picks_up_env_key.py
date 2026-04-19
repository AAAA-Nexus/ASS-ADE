# Extracted from C:/!ass-ade/tests/test_free_providers.py:156
# Component id: at.source.ass_ade.test_detect_picks_up_env_key
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_picks_up_env_key(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")
    available = detect_available_providers({})
    assert "groq" in {p.name for p in available}
