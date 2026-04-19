# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_gates.py:102
# Component id: at.source.ass_ade.test_certify_failed
__version__ = "0.1.0"

    def test_certify_failed(self):
        gates = QualityGates(_mock_nexus(rubric_passed=False, cert_score=0.3))
        result = gates.certify("bad code")
        assert result is not None
        assert result["passed"] is False
