# Extracted from C:/!ass-ade/tests/test_certifier.py:118
# Component id: at.source.ass_ade.test_render_certificate_text_contains_digest
from __future__ import annotations

__version__ = "0.1.0"

def test_render_certificate_text_contains_digest(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("x = 42\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path)
    text = render_certificate_text(cert)

    root_digest = cert["digest"]["root_digest"]
    # The render function truncates to 32 chars
    assert root_digest[:32] in text
