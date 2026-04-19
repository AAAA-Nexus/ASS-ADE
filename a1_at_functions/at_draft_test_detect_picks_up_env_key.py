# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_picks_up_env_key.py:7
# Component id: at.source.a1_at_functions.test_detect_picks_up_env_key
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_picks_up_env_key(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")
    available = detect_available_providers({})
    assert "groq" in {p.name for p in available}
