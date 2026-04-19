# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:14
# Component id: at.source.ass_ade.test_public_absolute_endpoint_allowed
__version__ = "0.1.0"

    def test_public_absolute_endpoint_allowed(self) -> None:
        """Public absolute endpoints should be allowed (when domain resolves)."""
        # Use a well-known public domain that should resolve
        result = _validate_absolute_endpoint("https://cloudflare.com/api/tool")
        assert result == "https://cloudflare.com/api/tool"
