# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_detect_test_framework_pytest.py:5
# Component id: at.source.ass_ade.test_detect_test_framework_pytest
__version__ = "0.1.0"

def test_detect_test_framework_pytest(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

    result = detect_test_framework(tmp_path)

    assert result == "pytest"
