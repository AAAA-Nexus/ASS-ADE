# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_errors.py:51
# Component id: at.source.ass_ade.test_2xx_does_nothing
__version__ = "0.1.0"

    def test_2xx_does_nothing(self) -> None:
        for code in (200, 201, 204, 299):
            raise_for_status(code)  # should not raise
