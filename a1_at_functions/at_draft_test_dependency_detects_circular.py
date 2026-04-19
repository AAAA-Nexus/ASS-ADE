# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_dependency_detects_circular.py:7
# Component id: at.source.a1_at_functions.test_dependency_detects_circular
from __future__ import annotations

__version__ = "0.1.0"

def test_dependency_detects_circular(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("from b import x\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("from a import y\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)
    assert result["has_circular_deps"] is True
