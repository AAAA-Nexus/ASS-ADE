# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:7
# Component id: sy.source.a4_sy_orchestration.testbuildsystemprompt
from __future__ import annotations

__version__ = "0.1.0"

class TestBuildSystemPrompt:
    def test_contains_working_dir(self, tmp_path):
        prompt = build_system_prompt(str(tmp_path))
        assert "ASS-ADE" in prompt
        assert str(tmp_path) in prompt

    def test_detects_python_project(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\n")
        prompt = build_system_prompt(str(tmp_path))
        assert "Python" in prompt

    def test_detects_node_project(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        prompt = build_system_prompt(str(tmp_path))
        assert "Node.js" in prompt
