# Extracted from C:/!ass-ade/tests/test_cli.py:138
# Component id: at.source.ass_ade.test_rebuild_dry_run_json
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_dry_run_json(tmp_path: Path) -> None:
    src = tmp_path / "myproject"
    src.mkdir()
    (src / "main.py").write_text("X = 1\n", encoding="utf-8")
    out = tmp_path / "myproject-rebuilt"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--dry-run", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True
    assert "by_tier" in payload
    assert not out.exists()
