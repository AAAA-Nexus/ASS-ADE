# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhancer.py:144
# Component id: at.source.ass_ade.test_scan_bare_except_typed_ok
__version__ = "0.1.0"

def test_scan_bare_except_typed_ok(tmp_path: Path) -> None:
    content = "try:\n    risky()\nexcept ValueError:\n    pass\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_bare_except(tmp_path)

    assert len(findings) == 0
