# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbasondmaxbreach.py:17
# Component id: at.source.ass_ade.test_d_max_breach_emits_bas_alert
__version__ = "0.1.0"

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
