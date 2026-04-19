# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:432
# Component id: at.source.ass_ade.test_cli_recon_missing_path
__version__ = "0.1.0"

def test_cli_recon_missing_path(tmp_path: Path) -> None:
    nonexistent = tmp_path / "does_not_exist"
    result = runner.invoke(app, ["recon", str(nonexistent)])
    assert result.exit_code != 0
