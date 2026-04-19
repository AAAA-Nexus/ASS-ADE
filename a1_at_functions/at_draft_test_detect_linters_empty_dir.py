# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_linters_empty_dir.py:7
# Component id: at.source.a1_at_functions.test_detect_linters_empty_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_linters_empty_dir(tmp_path: Path) -> None:
    result = detect_linters(tmp_path)

    assert isinstance(result, list)
