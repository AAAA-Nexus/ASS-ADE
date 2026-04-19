# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tier_aliases_include_canonical_and_claude.py:7
# Component id: at.source.a1_at_functions.test_tier_aliases_include_canonical_and_claude
from __future__ import annotations

__version__ = "0.1.0"

def test_tier_aliases_include_canonical_and_claude(self):
    assert TIER_ALIASES["haiku"] == TIER_FAST
    assert TIER_ALIASES["sonnet"] == TIER_BALANCED
    assert TIER_ALIASES["opus"] == TIER_DEEP
    assert TIER_ALIASES[TIER_FAST] == TIER_FAST
    assert TIER_ALIASES[TIER_BALANCED] == TIER_BALANCED
    assert TIER_ALIASES[TIER_DEEP] == TIER_DEEP
