# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_scan_missing_docs_private_ok.py:5
# Component id: at.source.ass_ade.test_scan_missing_docs_private_ok
__version__ = "0.1.0"

def test_scan_missing_docs_private_ok(tmp_path: Path) -> None:
    content = "def _private():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    # Private functions must not be flagged
    assert not any("_private" in f.get("title", "") for f in findings)
