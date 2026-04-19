# Extracted from C:/!ass-ade/tests/test_free_providers.py:252
# Component id: at.source.ass_ade.test_config_override_model_honored
from __future__ import annotations

__version__ = "0.1.0"

def test_config_override_model_honored(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    match = select_provider_for_tier(
        "balanced",
        config_providers={"groq": {"models_by_tier": {"balanced": "my-tuned-model"}}},
    )
    assert match is not None
    profile, model = match
    assert profile.name == "groq"
    assert model == "my-tuned-model"
