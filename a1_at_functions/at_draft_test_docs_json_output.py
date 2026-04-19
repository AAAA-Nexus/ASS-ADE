# Extracted from C:/!ass-ade/tests/test_new_codebase_commands.py:56
# Component id: at.source.ass_ade.test_docs_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_docs_json_output(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    payload = _extract_json(result.stdout)
    assert "files_generated" in payload
