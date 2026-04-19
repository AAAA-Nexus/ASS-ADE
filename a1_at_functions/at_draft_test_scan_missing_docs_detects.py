# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_missing_docs_detects.py:7
# Component id: at.source.a1_at_functions.test_scan_missing_docs_detects
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_missing_docs_detects(tmp_path: Path) -> None:
    content = "def public_function():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "missing_docs" for f in findings)
