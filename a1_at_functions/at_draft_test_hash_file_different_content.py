# Extracted from C:/!ass-ade/tests/test_certifier.py:32
# Component id: at.source.ass_ade.test_hash_file_different_content
from __future__ import annotations

__version__ = "0.1.0"

def test_hash_file_different_content(tmp_path: Path) -> None:
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    f1.write_bytes(b"x = 1")
    f2.write_bytes(b"x = 2")

    assert hash_file(f1) != hash_file(f2)
