# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:134
# Component id: at.source.ass_ade.test_fail_open_on_exception
__version__ = "0.1.0"

    def test_fail_open_on_exception(self):
        client = MagicMock()
        client.prompt_inject_scan.side_effect = Exception("network error")
        client.hallucination_oracle.side_effect = Exception("network error")
        client.security_shield.side_effect = Exception("network error")
        client.certify_output.side_effect = Exception("network error")
        gates = QualityGates(client)

        assert gates.scan_prompt("test") is None
        assert gates.check_hallucination("test") is None
        assert gates.shield_tool("x", {}) is None
        assert gates.certify("test") is None
