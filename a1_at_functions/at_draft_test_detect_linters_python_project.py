# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_linters_python_project.py:7
# Component id: at.source.a1_at_functions.test_detect_linters_python_project
from __future__ import annotations

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
