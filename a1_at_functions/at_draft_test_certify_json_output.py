# Extracted from C:/!ass-ade/tests/test_new_codebase_commands.py:108
# Component id: at.source.ass_ade.test_certify_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_json_output(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "schema" in payload
