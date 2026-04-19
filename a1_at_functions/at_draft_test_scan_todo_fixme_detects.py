# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhancer.py:158
# Component id: at.source.ass_ade.test_scan_todo_fixme_detects
__version__ = "0.1.0"

def test_scan_todo_fixme_detects(tmp_path: Path) -> None:
    content = "def do_work():\n    pass  # TODO: fix this later\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_todo_fixme(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "technical_debt" for f in findings)
