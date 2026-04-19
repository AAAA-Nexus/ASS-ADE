# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_scan_long_functions_detects.py:5
# Component id: at.source.ass_ade.test_scan_long_functions_detects
__version__ = "0.1.0"

def test_scan_long_functions_detects(tmp_path: Path) -> None:
    body_lines = "\n".join(f"    x_{i} = {i}" for i in range(60))
    content = f"def big_function():\n{body_lines}\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_long_functions(tmp_path)

    assert len(findings) >= 1
    assert findings[0]["category"] == "long_function"
