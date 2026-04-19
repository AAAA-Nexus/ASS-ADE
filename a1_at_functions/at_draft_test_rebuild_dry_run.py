# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rebuild_dry_run.py:7
# Component id: at.source.a1_at_functions.test_rebuild_dry_run
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_dry_run(tmp_path: Path) -> None:
    src = tmp_path / "myproject"
    src.mkdir()
    (src / "main.py").write_text("def hello(): pass\n", encoding="utf-8")
    out = tmp_path / "myproject-rebuilt"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--dry-run"])

    assert result.exit_code == 0
    assert "Dry-run preview" in result.stdout
    assert not out.exists(), "--dry-run must not create output folder"
