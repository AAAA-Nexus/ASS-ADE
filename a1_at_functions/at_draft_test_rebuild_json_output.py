# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_rebuild_json_output.py:7
# Component id: at.source.a1_at_functions.test_rebuild_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_json_output(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload.get("ok") is True
    assert "components_written" in payload
    assert "by_tier" in payload
