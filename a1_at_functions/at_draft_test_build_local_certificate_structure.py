# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_build_local_certificate_structure.py:7
# Component id: at.source.a1_at_functions.test_build_local_certificate_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_build_local_certificate_structure(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path)

    for key in ("schema", "version", "digest", "signed_by", "valid"):
        assert key in cert, f"missing key: {key}"
    assert cert["signed_by"] is None
    assert cert["valid"] is False
