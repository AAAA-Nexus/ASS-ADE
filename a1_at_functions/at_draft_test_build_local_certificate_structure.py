# Extracted from C:/!ass-ade/tests/test_certifier.py:94
# Component id: at.source.ass_ade.test_build_local_certificate_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_build_local_certificate_structure(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path)

    for key in ("schema", "version", "digest", "signed_by", "valid"):
        assert key in cert, f"missing key: {key}"
    assert cert["signed_by"] is None
    assert cert["valid"] is False
