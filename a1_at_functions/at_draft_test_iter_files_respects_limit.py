# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:138
# Component id: at.source.ass_ade.test_iter_files_respects_limit
from __future__ import annotations

__version__ = "0.1.0"

def test_iter_files_respects_limit(tmp_path: Path) -> None:
    for i in range(20):
        (tmp_path / f"f{i}.py").write_text("x=1", encoding="utf-8")
    files = _iter_files(tmp_path, limit=10)
    assert len(files) == 10
