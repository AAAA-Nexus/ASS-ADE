# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_hash_file_different_content.py:7
# Component id: at.source.a1_at_functions.test_hash_file_different_content
from __future__ import annotations

__version__ = "0.1.0"

def test_hash_file_different_content(tmp_path: Path) -> None:
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    f1.write_bytes(b"x = 1")
    f2.write_bytes(b"x = 2")

    assert hash_file(f1) != hash_file(f2)
