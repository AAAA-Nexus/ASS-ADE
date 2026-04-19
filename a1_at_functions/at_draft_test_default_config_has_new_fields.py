# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_default_config_has_new_fields.py:7
# Component id: at.source.a1_at_functions.test_default_config_has_new_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_default_config_has_new_fields(self):
    from ass_ade.config import AssAdeConfig
    cfg = AssAdeConfig()
    assert cfg.lse_enabled is True
    assert cfg.tier_policy == {}
    assert cfg.provider_fallback_chain == []
    assert cfg.providers == {}
