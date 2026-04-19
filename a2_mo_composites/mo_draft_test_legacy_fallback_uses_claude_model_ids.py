# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlseengine.py:72
# Component id: mo.source.ass_ade.test_legacy_fallback_uses_claude_model_ids
__version__ = "0.1.0"

    def test_legacy_fallback_uses_claude_model_ids(self):
        """When no free providers are configured, LSE falls back to Claude models."""
        from ass_ade.agent.lse import _LEGACY_TIER_TO_MODEL
        assert "claude" in _LEGACY_TIER_TO_MODEL["fast"]
        assert "claude" in _LEGACY_TIER_TO_MODEL["balanced"]
        assert "claude" in _LEGACY_TIER_TO_MODEL["deep"]
