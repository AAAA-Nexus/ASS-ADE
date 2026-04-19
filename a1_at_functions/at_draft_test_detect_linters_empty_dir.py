# Extracted from C:/!ass-ade/tests/test_linter.py:30
# Component id: at.source.ass_ade.test_detect_linters_empty_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_linters_empty_dir(tmp_path: Path) -> None:
    result = detect_linters(tmp_path)

    assert isinstance(result, list)
