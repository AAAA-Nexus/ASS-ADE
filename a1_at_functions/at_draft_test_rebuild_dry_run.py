# Extracted from C:/!ass-ade/tests/test_cli.py:125
# Component id: at.source.ass_ade.test_rebuild_dry_run
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
