# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a_cli.py:140
# Component id: at.source.ass_ade.test_local_card_displays
__version__ = "0.1.0"

    def test_local_card_displays(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card"])
        assert result.exit_code == 0
        assert "ASS-ADE" in result.stdout
