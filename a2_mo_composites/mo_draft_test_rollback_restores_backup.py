# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:237
# Component id: mo.source.ass_ade.test_rollback_restores_backup
__version__ = "0.1.0"

def test_rollback_restores_backup(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("v2\n", encoding="utf-8")

    backup = tmp_path / "myproject-backup-20240101-120000"
    backup.mkdir()
    (backup / "main.py").write_text("v1\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes"])

    assert result.exit_code == 0
    assert (target / "main.py").read_text(encoding="utf-8") == "v1\n"
