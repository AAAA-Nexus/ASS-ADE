# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_linters_returns_dict.py:7
# Component id: at.source.a1_at_functions.test_run_linters_returns_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_run_linters_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "hello.py").write_text("x = 1\n", encoding="utf-8")

    result = run_linters(tmp_path)

    assert isinstance(result, dict)
    assert "root" in result
    assert "linters_run" in result
    assert "results" in result
