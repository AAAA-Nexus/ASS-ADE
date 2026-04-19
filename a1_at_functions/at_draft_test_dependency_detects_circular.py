# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:192
# Component id: at.source.ass_ade.test_dependency_detects_circular
from __future__ import annotations

__version__ = "0.1.0"

def test_dependency_detects_circular(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("from b import x\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("from a import y\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)
    assert result["has_circular_deps"] is True
