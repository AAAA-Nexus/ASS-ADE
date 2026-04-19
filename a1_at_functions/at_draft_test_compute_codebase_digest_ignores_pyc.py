# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compute_codebase_digest_ignores_pyc.py:7
# Component id: at.source.a1_at_functions.test_compute_codebase_digest_ignores_pyc
from __future__ import annotations

__version__ = "0.1.0"

def test_compute_codebase_digest_ignores_pyc(tmp_path: Path) -> None:
    (tmp_path / "module.pyc").write_bytes(b"\x00\x01\x02")

    result = compute_codebase_digest(tmp_path)

    assert result["file_count"] == 0
    assert "module.pyc" not in result.get("files", {})
