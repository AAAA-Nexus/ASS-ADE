# Extracted from C:/!ass-ade/tests/test_enhancer.py:84
# Component id: at.source.ass_ade.test_scan_missing_docs_detects
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_missing_docs_detects(tmp_path: Path) -> None:
    content = "def public_function():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "missing_docs" for f in findings)
