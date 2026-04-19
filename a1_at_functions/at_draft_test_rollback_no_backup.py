# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rollback_no_backup.py:7
# Component id: at.source.a1_at_functions.test_rollback_no_backup
from __future__ import annotations

__version__ = "0.1.0"

def test_rollback_no_backup(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("pass\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes"])

    assert result.exit_code == 1
    assert "No backup" in result.stdout
