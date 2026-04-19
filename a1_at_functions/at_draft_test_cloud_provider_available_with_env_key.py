# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cloud_provider_available_with_env_key.py:7
# Component id: at.source.a1_at_functions.test_cloud_provider_available_with_env_key
from __future__ import annotations

__version__ = "0.1.0"

def test_cloud_provider_available_with_env_key(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")
    p = get_provider("groq")
    assert p.is_available() is True
