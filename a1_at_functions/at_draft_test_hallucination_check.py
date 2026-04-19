# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:116
# Component id: at.source.ass_ade.test_hallucination_check
__version__ = "0.1.0"

    def test_hallucination_check(self):
        gates = QualityGates(self._mock_client())
        result = gates.check_hallucination("The file has been fixed.")
        assert result is not None
        assert result["verdict"] == "safe"
