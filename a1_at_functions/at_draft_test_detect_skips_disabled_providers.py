# Extracted from C:/!ass-ade/tests/test_free_providers.py:151
# Component id: at.source.ass_ade.test_detect_skips_disabled_providers
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_skips_disabled_providers(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")
    available = detect_available_providers({"groq": {"enabled": False}})
    assert "groq" not in {p.name for p in available}
