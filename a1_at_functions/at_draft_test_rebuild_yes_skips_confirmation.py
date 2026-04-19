# Extracted from C:/!ass-ade/tests/test_cli.py:153
# Component id: at.source.ass_ade.test_rebuild_yes_skips_confirmation
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_yes_skips_confirmation(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify"])

    assert result.exit_code == 0
    assert out.exists()
