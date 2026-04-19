# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhance_cli.py:29
# Component id: at.source.ass_ade.test_enhance_help
__version__ = "0.1.0"

def test_enhance_help() -> None:
    result = runner.invoke(app, ["enhance", "--help"])

    assert result.exit_code == 0
    assert "enhance" in result.output.lower()
