# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testtrustgate.py:45
# Component id: at.source.ass_ade.test_validates_agent_id
__version__ = "0.1.0"

    def test_validates_agent_id(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            trust_gate(_mock_client(), "")
