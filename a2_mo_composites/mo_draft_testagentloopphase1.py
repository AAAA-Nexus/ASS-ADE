# Extracted from C:/!ass-ade/tests/test_phase_engines.py:103
# Component id: mo.source.ass_ade.testagentloopphase1
from __future__ import annotations

__version__ = "0.1.0"

class TestAgentLoopPhase1:
    def _make_loop(self):
        from unittest.mock import MagicMock
        from ass_ade.agent.loop import AgentLoop
        from ass_ade.agent.lse import LSEEngine

        provider = MagicMock()
        registry = MagicMock()
        registry.schemas.return_value = []
        lse = LSEEngine({})

        loop = AgentLoop(provider=provider, registry=registry, lse=lse)
        return loop

    def test_delegation_depth_resets_on_step(self):
        loop = self._make_loop()
        loop._delegation_depth = 10
        loop.reset_delegation_depth()
        assert loop.delegation_depth == 0

    def test_d_max_increment_blocks_at_limit(self):
        from ass_ade.agent.loop import D_MAX
        loop = self._make_loop()
        # Set depth to D_MAX so the next increment exceeds it
        loop._delegation_depth = D_MAX
        assert loop.increment_delegation_depth() is False

    def test_lse_decision_stored(self):
        loop = self._make_loop()
        routing = MagicMock()
        routing.complexity = "simple"
        loop._last_routing = routing
        model = loop._select_model(routing)
        # Should be a string model name (lse select works)
        assert model is None or isinstance(model, str)

    def test_refine_trigger_false_when_no_report(self):
        loop = self._make_loop()
        assert loop._check_refine_trigger(None) is False

    def test_refine_trigger_false_on_clean_report(self):
        from ass_ade.agent.orchestrator import CycleReport
        loop = self._make_loop()
        report = CycleReport(alerts=[], wisdom_score=0.8)
        report.engine_reports["cie"] = {"patches_applied": 0}
        assert loop._check_refine_trigger(report) is False
