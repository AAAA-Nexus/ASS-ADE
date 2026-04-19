# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_dependency_no_circular_clean_repo.py:7
# Component id: at.source.a1_at_functions.test_dependency_no_circular_clean_repo
from __future__ import annotations

__version__ = "0.1.0"

def test_dependency_no_circular_clean_repo(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("from utils import add\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)
    assert result["has_circular_deps"] is False
