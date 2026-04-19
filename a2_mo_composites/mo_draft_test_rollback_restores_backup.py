# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_rollback_restores_backup.py:7
# Component id: mo.source.a2_mo_composites.test_rollback_restores_backup
from __future__ import annotations

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
