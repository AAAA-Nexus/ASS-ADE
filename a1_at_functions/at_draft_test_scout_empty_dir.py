# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:172
# Component id: at.source.ass_ade.test_scout_empty_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_scout_empty_dir(tmp_path: Path) -> None:
    result = _scout_agent(tmp_path, [])
    assert result["total_files"] == 0
    assert result["total_size_kb"] == 0
