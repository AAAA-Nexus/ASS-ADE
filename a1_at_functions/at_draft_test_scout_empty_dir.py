# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scout_empty_dir.py:7
# Component id: at.source.a1_at_functions.test_scout_empty_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_scout_empty_dir(tmp_path: Path) -> None:
    result = _scout_agent(tmp_path, [])
    assert result["total_files"] == 0
    assert result["total_size_kb"] == 0
