# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentid.py:7
# Component id: at.source.a1_at_functions.testvalidateagentid
from __future__ import annotations

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
