# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:16
# Component id: sy.source.ass_ade.test_detects_node_project
__version__ = "0.1.0"

    def test_detects_node_project(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        prompt = build_system_prompt(str(tmp_path))
        assert "Node.js" in prompt
