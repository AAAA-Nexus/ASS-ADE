# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygatessam.py:27
# Component id: at.source.ass_ade.test_gate_sam_fail_open_on_exception
__version__ = "0.1.0"

    def test_gate_sam_fail_open_on_exception(self):
        from ass_ade.agent.gates import QualityGates
        broken_nexus = MagicMock()
        broken_nexus.trust_score.side_effect = RuntimeError("boom")
        gates = QualityGates(nexus_client=broken_nexus, config={})
        # Should not raise — context_memory may also raise; patch it
        with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2]):
            result = gates.gate_sam(target="x")
        # Either None (fail-open) or a dict
        assert result is None or isinstance(result, dict)
