# Extracted from C:/!ass-ade/tests/test_free_providers.py:657
# Component id: at.source.ass_ade.test_default_config_has_new_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_default_config_has_new_fields(self):
    from ass_ade.config import AssAdeConfig
    cfg = AssAdeConfig()
    assert cfg.lse_enabled is True
    assert cfg.tier_policy == {}
    assert cfg.provider_fallback_chain == []
    assert cfg.providers == {}
