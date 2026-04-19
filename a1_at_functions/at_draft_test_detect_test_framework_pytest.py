# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_test_framework_pytest.py:7
# Component id: at.source.a1_at_functions.test_detect_test_framework_pytest
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_test_framework_pytest(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

    result = detect_test_framework(tmp_path)

    assert result == "pytest"
