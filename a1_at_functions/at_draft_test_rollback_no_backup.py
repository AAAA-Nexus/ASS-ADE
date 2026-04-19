# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:226
# Component id: at.source.ass_ade.test_rollback_no_backup
__version__ = "0.1.0"

def test_rollback_no_backup(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("pass\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes"])

    assert result.exit_code == 1
    assert "No backup" in result.stdout
