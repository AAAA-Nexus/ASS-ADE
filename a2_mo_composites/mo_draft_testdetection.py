# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testdetection.py:7
# Component id: mo.source.a2_mo_composites.testdetection
from __future__ import annotations

__version__ = "0.1.0"

class TestDetection:
    def test_detect_returns_at_least_local_providers(self, monkeypatch):
        # Clear every cloud key
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        available = detect_available_providers({})
        names = {p.name for p in available}
        # Local providers + pollinations (no-key) must be available
        assert "ollama" in names
        assert "pollinations" in names

    def test_detect_skips_disabled_providers(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        available = detect_available_providers({"groq": {"enabled": False}})
        assert "groq" not in {p.name for p in available}

    def test_detect_picks_up_env_key(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        available = detect_available_providers({})
        assert "groq" in {p.name for p in available}

    def test_detect_config_key_overrides_env(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        available = detect_available_providers({"gemini": {"api_key": "config-key"}})
        assert "gemini" in {p.name for p in available}

    def test_provider_for_model_reverse_lookup(self):
        # groq's balanced tier model
        groq_balanced = get_provider("groq").models_by_tier["balanced"]
        assert provider_for_model(groq_balanced) == "groq"

    def test_provider_for_model_unknown_returns_none(self):
        assert provider_for_model("not-a-real-model") is None

    def test_provider_for_model_empty_string(self):
        assert provider_for_model("") is None
