# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_iter_files_respects_limit.py:7
# Component id: at.source.a1_at_functions.test_iter_files_respects_limit
from __future__ import annotations

__version__ = "0.1.0"

def test_iter_files_respects_limit(tmp_path: Path) -> None:
    for i in range(20):
        (tmp_path / f"f{i}.py").write_text("x=1", encoding="utf-8")
    files = _iter_files(tmp_path, limit=10)
    assert len(files) == 10
