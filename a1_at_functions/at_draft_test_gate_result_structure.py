# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_gates.py:135
# Component id: at.source.ass_ade.test_gate_result_structure
__version__ = "0.1.0"

    def test_gate_result_structure(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        result = gates.gate_log[0]
        assert isinstance(result, GateResult)
        assert result.gate == "prompt_scan"
        assert result.passed is True
        assert result.confidence > 0
