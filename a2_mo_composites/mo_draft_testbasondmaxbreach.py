# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase1_integration.py:161
# Component id: mo.source.ass_ade.testbasondmaxbreach
__version__ = "0.1.0"

class TestBASOnDMaxBreach:
    def test_d_max_breach_returns_blocked_message(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Simulate being inside a recursion by setting depth past D_MAX
        loop._delegation_depth = D_MAX + 1
        result = loop.step("[REFINE round 1/3] retry")
        assert "D_MAX" in result or "delegation" in result.lower()

    def test_d_max_breach_emits_bas_alert(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Set to exactly D_MAX so next increment exceeds
        loop._delegation_depth = D_MAX
        loop.step("[REFINE round 1/3] retry")

        # BAS should have a d_max_breach alert
        alerts = orchestrator.bas._alerts
        kinds = [a.kind for a in alerts]
        assert "d_max_breach" in kinds, f"Expected d_max_breach in {kinds}"

    def test_d_max_breach_severity_is_high(self):
        from ass_ade.agent.bas import _SEVERITY
        assert _SEVERITY.get("d_max_breach") == "high"

    def test_normal_flow_does_not_trigger_d_max_alert(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Normal step (depth = 0)
        loop.step("normal request")
        alerts = orchestrator.bas._alerts
        kinds = [a.kind for a in alerts]
        assert "d_max_breach" not in kinds
