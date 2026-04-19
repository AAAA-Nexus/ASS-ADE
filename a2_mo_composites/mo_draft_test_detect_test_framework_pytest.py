# Extracted from C:/!ass-ade/tests/test_docs_engine.py:119
# Component id: mo.source.ass_ade.test_detect_test_framework_pytest
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_test_framework_pytest(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

    result = detect_test_framework(tmp_path)

    assert result == "pytest"
