# Extracted from C:/!ass-ade/tests/test_new_codebase_commands.py:77
# Component id: at.source.ass_ade.test_lint_local_path
from __future__ import annotations

__version__ = "0.1.0"

def test_lint_local_path(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["lint", str(tmp_path), "--json"])

    assert result.exit_code in (0, 1)
    payload = _extract_json(result.stdout)
    assert "linters_run" in payload
