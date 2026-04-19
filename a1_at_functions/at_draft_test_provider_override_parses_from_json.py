# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_provider_override_parses_from_json.py:7
# Component id: at.source.a1_at_functions.test_provider_override_parses_from_json
from __future__ import annotations

__version__ = "0.1.0"

def test_provider_override_parses_from_json(self):
    from ass_ade.config import AssAdeConfig
    cfg = AssAdeConfig.model_validate({
        "profile": "local",
        "providers": {
            "groq": {"enabled": True, "api_key": "sk-test"},
            "gemini": {"enabled": False},
        },
        "tier_policy": {"balanced": "groq"},
        "provider_fallback_chain": ["groq", "gemini", "ollama"],
    })
    assert cfg.providers["groq"].api_key == "sk-test"
    assert cfg.providers["gemini"].enabled is False
    assert cfg.tier_policy == {"balanced": "groq"}
    assert cfg.provider_fallback_chain == ["groq", "gemini", "ollama"]
