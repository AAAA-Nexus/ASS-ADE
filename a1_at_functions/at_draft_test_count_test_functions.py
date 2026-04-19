# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_count_test_functions.py:7
# Component id: at.source.a1_at_functions.test_count_test_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_count_test_functions(tmp_path: Path) -> None:
    f = tmp_path / "test_utils.py"
    f.write_text(
        "def test_add(): assert True\ndef test_sub(): assert True\ndef helper(): pass\n",
        encoding="utf-8",
    )
    assert _count_test_functions(f) == 2
