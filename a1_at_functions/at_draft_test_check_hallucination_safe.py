# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:25
# Component id: at.source.ass_ade.test_check_hallucination_safe
__version__ = "0.1.0"

    def test_check_hallucination_safe(self):
        gates = QualityGates(_mock_nexus())
        result = gates.check_hallucination("Python is a programming language.")
        assert result is not None
        assert result["verdict"] == "safe"
        assert "policy_epsilon" in result
