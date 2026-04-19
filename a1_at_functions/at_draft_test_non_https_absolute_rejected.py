# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:50
# Component id: at.source.ass_ade.test_non_https_absolute_rejected
__version__ = "0.1.0"

    def test_non_https_absolute_rejected(self) -> None:
        """HTTP (non-HTTPS) absolute URLs should be rejected."""
        with pytest.raises(ValueError, match="https scheme"):
            _validate_absolute_endpoint("http://example.com/api")
