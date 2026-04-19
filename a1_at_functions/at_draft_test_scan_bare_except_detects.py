# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_bare_except_detects.py:7
# Component id: at.source.a1_at_functions.test_scan_bare_except_detects
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_bare_except_detects(tmp_path: Path) -> None:
    content = "try:\n    risky()\nexcept:\n    pass\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_bare_except(tmp_path)

    assert len(findings) >= 1
    assert findings[0]["category"] == "bare_except"
