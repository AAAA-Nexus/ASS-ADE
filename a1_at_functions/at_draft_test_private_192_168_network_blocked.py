# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:40
# Component id: at.source.ass_ade.test_private_192_168_network_blocked
__version__ = "0.1.0"

    def test_private_192_168_network_blocked(self) -> None:
        """Absolute URLs to 192.168.x.x should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://192.168.1.1/admin")
