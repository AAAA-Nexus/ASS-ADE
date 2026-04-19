# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_claude_tier_alias_in_tier_policy.py:7
# Component id: at.source.a1_at_functions.test_claude_tier_alias_in_tier_policy
from __future__ import annotations

__version__ = "0.1.0"

def test_claude_tier_alias_in_tier_policy(self):
    """tier_policy should accept 'haiku'/'sonnet'/'opus' aliases."""
    lse = self._make({"tier_policy": {"sonnet": "groq"}})
    # The policy key should have been normalized to 'balanced'
    assert lse._tier_policy == {"balanced": "groq"}
