# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testa2avalidatecli.py:27
# Component id: at.source.ass_ade.test_validate_missing_file
__version__ = "0.1.0"

    def test_validate_missing_file(self) -> None:
        result = runner.invoke(app, ["a2a", "validate", "/nonexistent/agent.json"])
        assert result.exit_code == 1
