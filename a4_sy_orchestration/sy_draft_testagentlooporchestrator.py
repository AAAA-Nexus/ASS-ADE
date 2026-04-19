# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:7
# Component id: sy.source.a2_mo_composites.testagentlooporchestrator
from __future__ import annotations

__version__ = "0.1.0"

class TestAgentLoopOrchestrator:
    def _make_loop(self, orchestrator=None):
        from ass_ade.agent.loop import AgentLoop
        from ass_ade.engine.provider import ModelProvider
        from ass_ade.engine.types import CompletionResponse, Message
        from ass_ade.tools.registry import default_registry

        mock_provider = MagicMock(spec=ModelProvider)
        mock_provider.complete.return_value = CompletionResponse(
            message=Message(role="assistant", content="Done.", tool_calls=[]),
            usage={"input_tokens": 10, "output_tokens": 5},
        )
        return AgentLoop(
            provider=mock_provider,
            registry=default_registry(),
            orchestrator=orchestrator,
        )

    def test_loop_accepts_orchestrator_param(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        assert loop._orchestrator is o

    def test_last_cycle_report_none_before_step(self) -> None:
        loop = self._make_loop()
        assert loop.last_cycle_report is None

    def test_last_cycle_report_set_after_step(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        loop.step("Write hello world")
        assert loop.last_cycle_report is not None
        assert isinstance(loop.last_cycle_report, CycleReport)

    def test_step_without_orchestrator_still_works(self) -> None:
        loop = self._make_loop(orchestrator=None)
        result = loop.step("Hello")
        assert isinstance(result, str)

    def test_orchestrator_on_step_start_called(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.return_value = {}
        o.on_tool_event.return_value = []
        o.on_step_end.return_value = CycleReport(alerts=[])

        loop = self._make_loop(orchestrator=o)
        loop.step("Do something")
        o.on_step_start.assert_called_once()

    def test_orchestrator_on_step_end_called(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.return_value = {}
        o.on_tool_event.return_value = []
        o.on_step_end.return_value = CycleReport(alerts=[])

        loop = self._make_loop(orchestrator=o)
        loop.step("Do something")
        o.on_step_end.assert_called_once()

    def test_orchestrator_error_does_not_block_loop(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.side_effect = RuntimeError("engine down")
        o.on_tool_event.side_effect = RuntimeError("engine down")
        o.on_step_end.side_effect = RuntimeError("engine down")

        loop = self._make_loop(orchestrator=o)
        # Should not raise — fail-open design
        result = loop.step("Do something")
        assert isinstance(result, str)
