# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:25
# Component id: at.source.ass_ade.test_loopback_127_0_0_1_blocked
__version__ = "0.1.0"

    def test_loopback_127_0_0_1_blocked(self) -> None:
        """Absolute URLs to 127.0.0.1 should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://127.0.0.1/admin")
