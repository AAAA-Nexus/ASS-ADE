# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_linter.py:17
# Component id: at.source.ass_ade.test_detect_linters_python_project
__version__ = "0.1.0"

def test_detect_linters_python_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[tool.ruff]\nline-length = 88\n",
        encoding="utf-8",
    )

    # Ensure shutil.which("ruff") returns a truthy value so the linter is detected
    with patch("ass_ade.local.linter.shutil.which", side_effect=lambda cmd: cmd if cmd == "ruff" else None):
        result = detect_linters(tmp_path)

    assert "ruff" in result
