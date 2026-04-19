# Extracted from C:/!ass-ade/tests/test_free_providers.py:161
# Component id: at.source.ass_ade.test_detect_config_key_overrides_env
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_config_key_overrides_env(self, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    available = detect_available_providers({"gemini": {"api_key": "config-key"}})
    assert "gemini" in {p.name for p in available}
