# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_routing.py:113
# Component id: at.source.ass_ade.test_route_with_nexus_recommendation
__version__ = "0.1.0"

    def test_route_with_nexus_recommendation(self):
        nexus = type("NexusMock", (), {
            "routing_recommend": lambda self, **kwargs: {
                "model": "claude-sonnet-4",
                "reason": "Nexus route picked for balanced complexity",
                "confidence": 0.62,
                "tier": "standard",
            }
        })()
        router = EpistemicRouter(nexus_client=nexus)
        decision = router.route("Hello")
        assert decision.source == "nexus"
        assert decision.recommended_model == "claude-sonnet-4"
        assert decision.reason == "Nexus route picked for balanced complexity"
        assert decision.tier == ModelTier.STANDARD
        assert decision.complexity == 0.62
