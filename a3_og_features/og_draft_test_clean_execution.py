# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testsafeexecute.py:6
# Component id: og.source.ass_ade.test_clean_execution
__version__ = "0.1.0"

    def test_clean_execution(self) -> None:
        result = safe_execute(_mock_client(), "search_web", "query text", agent_id="13608")
        assert result.shield_passed is True
        assert result.prompt_scan_passed is True
