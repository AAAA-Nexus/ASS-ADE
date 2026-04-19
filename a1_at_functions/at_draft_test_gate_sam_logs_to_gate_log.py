# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygatessam.py:22
# Component id: at.source.ass_ade.test_gate_sam_logs_to_gate_log
__version__ = "0.1.0"

    def test_gate_sam_logs_to_gate_log(self):
        gates = self._make_gates()
        gates.gate_sam(target="x")
        assert any(g.gate == "sam" for g in gates.gate_log)
