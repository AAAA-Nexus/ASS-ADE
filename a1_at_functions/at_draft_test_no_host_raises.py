# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_validation.py:117
# Component id: at.source.ass_ade.test_no_host_raises
__version__ = "0.1.0"

    def test_no_host_raises(self) -> None:
        with pytest.raises(ValueError, match="valid host"):
            validate_url("https://")
