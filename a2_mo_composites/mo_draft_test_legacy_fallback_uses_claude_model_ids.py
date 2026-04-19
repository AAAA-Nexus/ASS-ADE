# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseengine.py:74
# Component id: mo.source.a2_mo_composites.test_legacy_fallback_uses_claude_model_ids
from __future__ import annotations

__version__ = "0.1.0"

def test_legacy_fallback_uses_claude_model_ids(self):
    """When no free providers are configured, LSE falls back to Claude models."""
    from ass_ade.agent.lse import _LEGACY_TIER_TO_MODEL
    assert "claude" in _LEGACY_TIER_TO_MODEL["fast"]
    assert "claude" in _LEGACY_TIER_TO_MODEL["balanced"]
    assert "claude" in _LEGACY_TIER_TO_MODEL["deep"]
