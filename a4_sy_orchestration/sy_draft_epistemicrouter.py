# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_epistemicrouter.py:7
# Component id: sy.source.a4_sy_orchestration.epistemicrouter
from __future__ import annotations

__version__ = "0.1.0"

class EpistemicRouter:
    """Stateful router that tracks routing history for session analytics."""

    def __init__(self, nexus_client: Any = None) -> None:
        self._nexus = nexus_client
        self._history: list[RoutingDecision] = []

    def route(self, message: str) -> RoutingDecision:
        """Route a message using best available method."""
        if self._nexus is not None:
            try:
                result = self._nexus.routing_recommend(prompt=message)
                confidence = _result_field(result, "confidence")
                if isinstance(confidence, (int, float)):
                    complexity = max(0.0, min(1.0, float(confidence)))
                else:
                    complexity = classify_complexity(message)

                model_name = _result_field(result, "model") or _result_field(result, "recommended_model")
                reason = _result_field(result, "reason", "Nexus recommendation")

                decision = RoutingDecision(
                    tier=_nexus_tier(result),
                    complexity=complexity,
                    recommended_model=str(model_name) if model_name else None,
                    reason=str(reason),
                    source="nexus",
                )
            except Exception:
                decision = local_route(message)
        else:
            decision = local_route(message)
        self._history.append(decision)
        return decision

    @property
    def history(self) -> list[RoutingDecision]:
        return list(self._history)

    @property
    def avg_complexity(self) -> float:
        """Average complexity across all routed messages."""
        if not self._history:
            return 0.0
        return sum(d.complexity for d in self._history) / len(self._history)
