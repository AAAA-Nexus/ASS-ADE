# Extracted from C:/!ass-ade/tests/test_certifier.py:21
# Component id: at.source.ass_ade.test_hash_file_deterministic
from __future__ import annotations

__version__ = "0.1.0"

def test_hash_file_deterministic(tmp_path: Path) -> None:
    f = tmp_path / "sample.py"
    f.write_bytes(b"def hello(): pass\n")

    h1 = hash_file(f)
    h2 = hash_file(f)

    assert h1 == h2
    assert len(h1) == 64  # sha256 hex digest length
