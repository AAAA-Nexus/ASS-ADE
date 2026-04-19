# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lint_local_path.py:7
# Component id: at.source.a1_at_functions.test_lint_local_path
from __future__ import annotations

__version__ = "0.1.0"

def test_lint_local_path(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["lint", str(tmp_path), "--json"])

    assert result.exit_code in (0, 1)
    payload = _extract_json(result.stdout)
    assert "linters_run" in payload
