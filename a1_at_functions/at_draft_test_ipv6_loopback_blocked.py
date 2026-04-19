# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:45
# Component id: at.source.ass_ade.test_ipv6_loopback_blocked
__version__ = "0.1.0"

    def test_ipv6_loopback_blocked(self) -> None:
        """Absolute URLs to IPv6 loopback should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://[::1]/admin")
