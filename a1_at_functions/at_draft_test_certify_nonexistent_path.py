# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_codebase_commands.py:118
# Component id: at.source.ass_ade.test_certify_nonexistent_path
__version__ = "0.1.0"

def test_certify_nonexistent_path() -> None:
    result = runner.invoke(app, ["certify", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1
