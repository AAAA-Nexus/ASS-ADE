# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rebuild_dry_run_json.py:7
# Component id: at.source.a1_at_functions.test_rebuild_dry_run_json
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
