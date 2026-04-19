# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_security_patterns_eval.py:7
# Component id: at.source.a1_at_functions.test_scan_security_patterns_eval
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_security_patterns_eval(tmp_path: Path) -> None:
    content = "output = eval(user_input)\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_security_patterns(tmp_path)

    assert any(f["category"] == "security" for f in findings)
    assert any("eval" in f["title"].lower() for f in findings)
