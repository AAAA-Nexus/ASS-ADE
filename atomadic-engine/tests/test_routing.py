"""Tests for agent.routing — epistemic model routing."""

from __future__ import annotations

from ass_ade.agent.routing import (
    EpistemicRouter,
    ModelTier,
    RoutingDecision,
    classify_complexity,
    local_route,
    tier_for_complexity,
)


class TestClassifyComplexity:
    def test_simple_greeting(self):
        c = classify_complexity("Hello!")
        assert c < 0.3

    def test_code_request(self):
        c = classify_complexity("Write a Python function to sort a list")
        assert c >= 0.3  # code keywords

    def test_complex_multi_step(self):
        c = classify_complexity(
            "First, implement a REST API endpoint for user registration, "
            "then write integration tests and create a database migration"
        )
        assert c >= 0.5

    def test_formal_verification(self):
        c = classify_complexity(
            "Write a formal proof that this invariant holds across all states"
        )
        assert c >= 0.2  # formal keywords detected

    def test_long_text_adds_complexity(self):
        short = classify_complexity("Fix the bug")
        long_ = classify_complexity("Fix the bug " + "detailed context " * 100)
        assert long_ > short

    def test_range_bounded(self):
        c = classify_complexity(
            "First implement a function, then write a theorem proof, "
            "design the architecture, and create several test files " * 10
        )
        assert c <= 1.0

    def test_empty_string(self):
        assert classify_complexity("") == 0.0


class TestTierForComplexity:
    def test_fast(self):
        assert tier_for_complexity(0.1) == ModelTier.FAST

    def test_standard(self):
        assert tier_for_complexity(0.4) == ModelTier.STANDARD

    def test_deep(self):
        assert tier_for_complexity(0.8) == ModelTier.DEEP

    def test_boundary_fast_standard(self):
        assert tier_for_complexity(0.29) == ModelTier.FAST
        assert tier_for_complexity(0.3) == ModelTier.STANDARD

    def test_boundary_standard_deep(self):
        assert tier_for_complexity(0.59) == ModelTier.STANDARD
        assert tier_for_complexity(0.6) == ModelTier.DEEP


class TestLocalRoute:
    def test_simple_query(self):
        decision = local_route("What is 2 + 2?")
        assert decision.tier == ModelTier.FAST
        assert decision.source == "local"
        assert decision.recommended_model is not None

    def test_code_query(self):
        decision = local_route("Write a function to parse JSON")
        assert decision.tier in (ModelTier.STANDARD, ModelTier.DEEP)
        assert decision.complexity >= 0.3

    def test_decision_has_reason(self):
        decision = local_route("Hello")
        assert "heuristic" in decision.reason.lower()


class TestEpistemicRouter:
    def test_route_without_nexus(self):
        router = EpistemicRouter()
        decision = router.route("Hello world")
        assert isinstance(decision, RoutingDecision)
        assert decision.source == "local"

    def test_history_tracking(self):
        router = EpistemicRouter()
        router.route("Hello")
        router.route("Write a complex algorithm with formal proof")
        assert len(router.history) == 2

    def test_avg_complexity(self):
        router = EpistemicRouter()
        router.route("Hi")
        router.route("Write code")
        avg = router.avg_complexity
        assert 0 <= avg <= 1.0

    def test_avg_complexity_empty(self):
        router = EpistemicRouter()
        assert router.avg_complexity == 0.0

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

    def test_route_with_nexus_exception_falls_back_local(self):
        nexus = type("NexusBoom", (), {
            "routing_recommend": lambda self, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
        })()
        router = EpistemicRouter(nexus_client=nexus)
        decision = router.route("Write a function to parse JSON")
        assert decision.source == "local"
