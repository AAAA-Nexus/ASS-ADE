# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_gates.py:51
# Component id: at.source.ass_ade.test_scan_prompt_clean
__version__ = "0.1.0"

    def test_scan_prompt_clean(self):
        gates = QualityGates(_mock_nexus())
        result = gates.scan_prompt("What is Python?")
        assert result is not None
        assert result["blocked"] is False
