# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_docs_nonexistent_path.py:5
# Component id: at.source.ass_ade.test_docs_nonexistent_path
__version__ = "0.1.0"

def test_docs_nonexistent_path() -> None:
    result = runner.invoke(app, ["docs", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1
