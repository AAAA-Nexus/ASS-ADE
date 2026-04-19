# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:5
# Component id: sy.source.ass_ade.testbuildsystemprompt
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
