# Extracted from C:/!ass-ade/tests/test_free_providers.py:70
# Component id: at.source.ass_ade.test_tier_aliases_include_canonical_and_claude
from __future__ import annotations

__version__ = "0.1.0"

def test_tier_aliases_include_canonical_and_claude(self):
    assert TIER_ALIASES["haiku"] == TIER_FAST
    assert TIER_ALIASES["sonnet"] == TIER_BALANCED
    assert TIER_ALIASES["opus"] == TIER_DEEP
    assert TIER_ALIASES[TIER_FAST] == TIER_FAST
    assert TIER_ALIASES[TIER_BALANCED] == TIER_BALANCED
    assert TIER_ALIASES[TIER_DEEP] == TIER_DEEP
