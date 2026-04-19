# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:74
# Component id: at.source.ass_ade.test_detects_node_project
__version__ = "0.1.0"

    def test_detects_node_project(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        prompt = build_system_prompt(str(tmp_path))
        assert "Node.js" in prompt
