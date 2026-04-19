# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detects_python_project.py:7
# Component id: at.source.a1_at_functions.test_detects_python_project
from __future__ import annotations

__version__ = "0.1.0"

def test_detects_python_project(self, tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\n")
    prompt = build_system_prompt(str(tmp_path))
    assert "Python" in prompt
