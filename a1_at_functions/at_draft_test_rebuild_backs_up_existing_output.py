# Extracted from C:/!ass-ade/tests/test_cli.py:180
# Component id: at.source.ass_ade.test_rebuild_backs_up_existing_output
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_backs_up_existing_output(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"
    out.mkdir()
    (out / "old.txt").write_text("old output\n", encoding="utf-8")

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    backup_path = Path(payload["output_backup"])
    assert backup_path.exists()
    assert (backup_path / "old.txt").read_text(encoding="utf-8") == "old output\n"
