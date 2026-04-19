# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_docs_json_output.py:5
# Component id: at.source.ass_ade.test_docs_json_output
__version__ = "0.1.0"

def test_docs_json_output(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "files_generated" in payload
