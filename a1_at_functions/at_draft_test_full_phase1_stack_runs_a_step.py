# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:254
# Component id: at.source.ass_ade.test_full_phase1_stack_runs_a_step
from __future__ import annotations

__version__ = "0.1.0"

def test_full_phase1_stack_runs_a_step(self):
    nexus = _make_nexus_mock()
    gates = QualityGates(nexus, config={})
    orchestrator = EngineOrchestrator({}, nexus=nexus)
    lse = LSEEngine({})
    provider = _make_provider_returning_text("done")
    registry = ToolRegistry()

    loop = AgentLoop(
        provider=provider,
        registry=registry,
        quality_gates=gates,
        orchestrator=orchestrator,
        lse=lse,
    )

    with patch("ass_ade.context_memory.vector_embed", return_value=[0.3] * 8):
        result = loop.step("what is Python's GIL?")

    assert result == "done"
    # SAM ran
    assert loop.last_sam_result is not None
    # LSE chose a model
    assert loop.last_lse_decision is not None
    # CycleReport was produced
    assert loop.last_cycle_report is not None
    # Delegation depth back to 0 after step
    assert loop.delegation_depth == 0
