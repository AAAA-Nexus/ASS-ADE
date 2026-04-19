# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:258
# Component id: at.source.ass_ade.test_count_test_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_count_test_functions(tmp_path: Path) -> None:
    f = tmp_path / "test_utils.py"
    f.write_text(
        "def test_add(): assert True\ndef test_sub(): assert True\ndef helper(): pass\n",
        encoding="utf-8",
    )
    assert _count_test_functions(f) == 2
