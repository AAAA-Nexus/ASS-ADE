# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_scan_missing_docs_detects.py:5
# Component id: at.source.ass_ade.test_scan_missing_docs_detects
__version__ = "0.1.0"

def test_scan_missing_docs_detects(tmp_path: Path) -> None:
    content = "def public_function():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "missing_docs" for f in findings)
