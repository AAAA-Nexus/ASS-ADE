# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_auto_detect_helper.py:7
# Component id: at.source.a1_at_functions.test_auto_detect_helper
from __future__ import annotations

__version__ = "0.1.0"

def test_auto_detect_helper(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "util.py").write_text("def f(): pass\n", encoding="utf-8")

    from ass_ade.cli import _auto_detect_project
    result = _auto_detect_project(tmp_path)

    assert "Python" in result
    assert "files" in result
    assert "Try:" in result
