# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:32
# Component id: at.source.ass_ade.test_check_hallucination_unsafe
__version__ = "0.1.0"

    def test_check_hallucination_unsafe(self):
        gates = QualityGates(_mock_nexus(verdict="unsafe", policy_epsilon=0.85))
        result = gates.check_hallucination("Made up claim.")
        assert result is not None
        assert result["verdict"] == "unsafe"
