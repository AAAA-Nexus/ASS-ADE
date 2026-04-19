# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_validation.py:113
# Component id: at.source.ass_ade.test_ftp_raises
__version__ = "0.1.0"

    def test_ftp_raises(self) -> None:
        with pytest.raises(ValueError, match="http or https"):
            validate_url("ftp://example.com")
