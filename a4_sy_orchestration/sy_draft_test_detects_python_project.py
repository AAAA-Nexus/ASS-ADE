# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:13
# Component id: sy.source.a4_sy_orchestration.test_detects_python_project
from __future__ import annotations

__version__ = "0.1.0"

def test_detects_python_project(self, tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\n")
    prompt = build_system_prompt(str(tmp_path))
    assert "Python" in prompt
