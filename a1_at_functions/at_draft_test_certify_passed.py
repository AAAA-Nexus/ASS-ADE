# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:50
# Component id: at.source.ass_ade.test_certify_passed
__version__ = "0.1.0"

    def test_certify_passed(self):
        gates = QualityGates(_mock_nexus())
        result = gates.certify("def add(a, b): return a + b")
        assert result is not None
        assert result["passed"] is True
        assert result["certificate_id"] == "cert-123"
