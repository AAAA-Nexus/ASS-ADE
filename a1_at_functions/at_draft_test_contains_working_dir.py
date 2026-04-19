# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:64
# Component id: at.source.ass_ade.test_contains_working_dir
__version__ = "0.1.0"

    def test_contains_working_dir(self, tmp_path):
        prompt = build_system_prompt(str(tmp_path))
        assert "ASS-ADE" in prompt
        assert str(tmp_path) in prompt
