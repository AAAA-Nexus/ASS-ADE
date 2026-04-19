# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_certify_json_output.py:7
# Component id: at.source.a1_at_functions.test_certify_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_json_output(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "schema" in payload
