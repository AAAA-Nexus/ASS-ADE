# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_codebase_commands.py:46
# Component id: at.source.ass_ade.test_docs_local_only
__version__ = "0.1.0"

def test_docs_local_only(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    # Should report how many docs were written
    assert "docs written" in result.stdout or "written" in result.stdout.lower()
