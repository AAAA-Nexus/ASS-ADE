# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhancer.py:119
# Component id: at.source.ass_ade.test_scan_security_patterns_eval
__version__ = "0.1.0"

def test_scan_security_patterns_eval(tmp_path: Path) -> None:
    content = "output = eval(user_input)\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_security_patterns(tmp_path)

    assert any(f["category"] == "security" for f in findings)
    assert any("eval" in f["title"].lower() for f in findings)
