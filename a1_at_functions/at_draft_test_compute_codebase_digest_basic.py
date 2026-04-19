# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compute_codebase_digest_basic.py:7
# Component id: at.source.a1_at_functions.test_compute_codebase_digest_basic
from __future__ import annotations

__version__ = "0.1.0"

def test_compute_codebase_digest_basic(tmp_path: Path) -> None:
    (tmp_path / "alpha.py").write_text("a = 1\n", encoding="utf-8")
    (tmp_path / "beta.py").write_text("b = 2\n", encoding="utf-8")

    result = compute_codebase_digest(tmp_path)

    assert "root_digest" in result
    assert result["file_count"] == 2
    assert "files" in result
    assert isinstance(result["files"], dict)
