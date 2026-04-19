# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_detect_languages_ignores_venv.py:5
# Component id: at.source.ass_ade.test_detect_languages_ignores_venv
__version__ = "0.1.0"

def test_detect_languages_ignores_venv(tmp_path: Path) -> None:
    venv = tmp_path / ".venv" / "lib"
    venv.mkdir(parents=True)
    (venv / "something.py").write_text("pass", encoding="utf-8")
    # Also add a real py file so the dict is non-empty in a different ext
    (tmp_path / "real.txt").write_text("x", encoding="utf-8")

    result = detect_languages(tmp_path)

    assert "py" not in result, ".venv .py files should be excluded"
