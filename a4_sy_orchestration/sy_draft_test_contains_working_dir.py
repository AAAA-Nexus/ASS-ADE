# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:6
# Component id: sy.source.ass_ade.test_contains_working_dir
__version__ = "0.1.0"

    def test_contains_working_dir(self, tmp_path):
        prompt = build_system_prompt(str(tmp_path))
        assert "ASS-ADE" in prompt
        assert str(tmp_path) in prompt
