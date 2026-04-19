# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_build_local_certificate_version.py:7
# Component id: at.source.a1_at_functions.test_build_local_certificate_version
from __future__ import annotations

__version__ = "0.1.0"

def test_build_local_certificate_version(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path, version="1.2.3")

    assert cert["version"] == "1.2.3"
