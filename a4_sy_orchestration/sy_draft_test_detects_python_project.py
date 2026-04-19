# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:11
# Component id: sy.source.ass_ade.test_detects_python_project
__version__ = "0.1.0"

    def test_detects_python_project(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\n")
        prompt = build_system_prompt(str(tmp_path))
        assert "Python" in prompt
