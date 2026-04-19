# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygatessam.py:13
# Component id: at.source.ass_ade.test_gate_sam_returns_dict
__version__ = "0.1.0"

    def test_gate_sam_returns_dict(self):
        gates = self._make_gates()
        result = gates.gate_sam(target="test_target")
        assert result is not None
        assert "trs" in result
        assert "g23" in result
        assert "composite" in result
        assert "passed" in result
