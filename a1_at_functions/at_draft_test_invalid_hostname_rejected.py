# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:55
# Component id: at.source.ass_ade.test_invalid_hostname_rejected
__version__ = "0.1.0"

    def test_invalid_hostname_rejected(self) -> None:
        """Absolute URLs with invalid hostnames should be rejected."""
        with pytest.raises(ValueError, match="valid host"):
            _validate_absolute_endpoint("https:///api")
