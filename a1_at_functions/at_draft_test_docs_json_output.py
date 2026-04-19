# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_docs_json_output.py:7
# Component id: at.source.a1_at_functions.test_docs_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_docs_json_output(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "files_generated" in payload
