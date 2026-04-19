# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:252
# Component id: at.source.ass_ade.test_rollback_json
__version__ = "0.1.0"

def test_rollback_json(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("v2\n", encoding="utf-8")

    backup = tmp_path / "myproject-backup-20240101-120000"
    backup.mkdir()
    (backup / "main.py").write_text("v1\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert "backup_name" in payload
