# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_validation.py:15
# Component id: at.source.ass_ade.testvalidateagentid
__version__ = "0.1.0"

class TestValidateAgentId:
    def test_valid_ids(self) -> None:
        assert validate_agent_id("agent-1") == "agent-1"
        assert validate_agent_id("13608") == "13608"
        assert validate_agent_id("my_agent.v2:latest") == "my_agent.v2:latest"

    def test_strips_whitespace(self) -> None:
        assert validate_agent_id("  agent-1  ") == "agent-1"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_agent_id("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_agent_id("   ")

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_agent_id("a" * 257)

    def test_invalid_chars_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent id with spaces")
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent<script>")
