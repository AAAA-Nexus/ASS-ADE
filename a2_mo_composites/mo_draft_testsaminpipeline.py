# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testsaminpipeline.py:5
# Component id: mo.source.ass_ade.testsaminpipeline
__version__ = "0.1.0"

class TestSAMInPipeline:
    def test_sam_runs_first_in_pipeline(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2, 0.3]):
            results = gates.run_pipeline(prompt="build a function", output="def x(): pass")
        gate_names = [r.gate for r in results]
        assert "sam" in gate_names, f"SAM missing from pipeline: {gate_names}"
        # SAM must be the very first gate
        assert gate_names[0] == "sam"

    def test_sam_pipeline_passes_intent_and_impl(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        with patch("ass_ade.context_memory.vector_embed", return_value=[0.5, 0.5, 0.5]):
            results = gates.run_pipeline(
                prompt="add input validation",
                output="def f(x): assert x",
                intent="add input validation",
                impl="def f(x): assert x",
            )
        sam_result = next((r for r in results if r.gate == "sam"), None)
        assert sam_result is not None
        assert sam_result.details is not None
        assert "trs" in sam_result.details
        assert "g23" in sam_result.details
