# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:69
# Component id: at.source.ass_ade.test_detects_python_project
__version__ = "0.1.0"

    def test_detects_python_project(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\n")
        prompt = build_system_prompt(str(tmp_path))
        assert "Python" in prompt
