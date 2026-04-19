# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_docs_local_only.py:7
# Component id: at.source.a1_at_functions.test_docs_local_only
from __future__ import annotations

__version__ = "0.1.0"

def test_docs_local_only(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)

    result = runner.invoke(app, ["docs", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    # Should report how many docs were written
    assert "docs written" in result.stdout or "written" in result.stdout.lower()
