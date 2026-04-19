# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_config_override_model_honored.py:7
# Component id: at.source.a1_at_functions.test_config_override_model_honored
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
