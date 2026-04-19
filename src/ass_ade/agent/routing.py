"""Epistemic routing — model selection based on task complexity.

In premium/hybrid mode, ASS-ADE delegates model selection to AAAA-Nexus
using routing_think() and routing_recommend() to find the optimal model
for each query. In local mode, a heuristic classifier is used.

The routing decision considers:
  - Estimated task complexity (code generation, analysis, simple Q&A)
  - Available models and their capabilities
  - Token budget constraints
  - Quality gate requirements

Local heuristic classification (no Nexus required):

    Task complexity C is estimated from the last user message:
      C_code   = 0.3 if code keywords present, else 0
      C_length = min(0.3, len(message) / 3000)
      C_multi  = 0.2 if multi-step indicators found, else 0
      C_formal = 0.2 if formal/proof keywords found, else 0
      C = C_code + C_length + C_multi + C_formal   ∈ [0, 1]

    Model tier:
      C < 0.3  → FAST   (small/cheap model)
      C < 0.6  → STANDARD (general purpose)
      C ≥ 0.6  → DEEP   (large/reasoning model)
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ModelTier(str, Enum):
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"


# Regex patterns for heuristic classification
_CODE_PATTERN = re.compile(
    r"\b(function|def |class |impl |fn |async |import |from |const |let |var |"
    r"write.*code|implement|refactor|debug|fix.*bug|compile|build|test|"
    r"api|endpoint|database|schema|migration)\b",
    re.IGNORECASE,
)
_MULTI_STEP_PATTERN = re.compile(
    r"\b(first.*then|step \d|multiple|several|all of|each of|"
    r"plan|design|architect|review.*and.*fix|create.*and.*test)\b",
    re.IGNORECASE,
)
_FORMAL_PATTERN = re.compile(
    r"\b(proof|theorem|verify|formal|invariant|correctness|"
    r"specification|guarantee|mathematical|axiom|lemma)\b",
    re.IGNORECASE,
)

# Model name suggestions per tier
_TIER_MODELS: dict[ModelTier, list[str]] = {
    ModelTier.FAST: [
        "gpt-4o-mini",
        "claude-3.5-haiku",
        "gemini-2.0-flash",
        "llama-3.1-8b",
    ],
    ModelTier.STANDARD: [
        "gpt-4o",
        "claude-3.7-sonnet",
        "claude-sonnet-4",
        "gemini-2.5-flash",
        "llama-3.3-70b",
    ],
    ModelTier.DEEP: [
        "o3",
        "o4-mini",
        "claude-opus-4",
        "gemini-2.5-pro",
        "deepseek-r1",
    ],
}


@dataclass
class RoutingDecision:
    """Result of an epistemic routing decision."""

    tier: ModelTier
    complexity: float  # ∈ [0, 1]
    recommended_model: str | None = None
    reason: str = ""
    source: str = "local"  # "local" | "nexus"


def classify_complexity(message: str) -> float:
    """Estimate task complexity from a user message.

    Returns a score in [0, 1].
    """
    c_code = 0.3 if _CODE_PATTERN.search(message) else 0.0
    c_length = min(0.3, len(message) / 3000)
    c_multi = 0.2 if _MULTI_STEP_PATTERN.search(message) else 0.0
    c_formal = 0.2 if _FORMAL_PATTERN.search(message) else 0.0
    return min(1.0, c_code + c_length + c_multi + c_formal)


def tier_for_complexity(complexity: float) -> ModelTier:
    """Map a complexity score to a model tier."""
    if complexity < 0.3:
        return ModelTier.FAST
    elif complexity < 0.6:
        return ModelTier.STANDARD
    else:
        return ModelTier.DEEP


def local_route(message: str) -> RoutingDecision:
    """Route using local heuristics (no Nexus required)."""
    c = classify_complexity(message)
    tier = tier_for_complexity(c)
    candidates = _TIER_MODELS.get(tier, [])
    return RoutingDecision(
        tier=tier,
        complexity=c,
        recommended_model=candidates[0] if candidates else None,
        reason=f"Local heuristic: complexity={c:.2f} → {tier.value}",
        source="local",
    )


async def nexus_route(
    message: str,
    nexus_client: Any,
    available_models: list[str] | None = None,
) -> RoutingDecision:
    """Route using AAAA-Nexus epistemic routing endpoints.

    Falls back to local routing if Nexus is unavailable.
    """
    try:
        result = nexus_client.routing_recommend(
            prompt=message,
            available_models=available_models or [],
        )
        return RoutingDecision(
            tier=_nexus_tier(result),
            complexity=getattr(result, "complexity", 0.5),
            recommended_model=getattr(result, "recommended_model", None),
            reason=getattr(result, "reason", "Nexus recommendation"),
            source="nexus",
        )
    except Exception:
        return local_route(message)


def _nexus_tier(result: Any) -> ModelTier:
    """Extract tier from a Nexus routing response."""
    if isinstance(result, Mapping):
        raw = result.get("tier")
        if isinstance(raw, str):
            tier_str = raw.lower()
        else:
            tier_str = "standard"
    else:
        tier_str = str(getattr(result, "tier", "standard")).lower()
    try:
        return ModelTier(tier_str)
    except ValueError:
        return ModelTier.STANDARD


def _result_field(result: Any, key: str, default: Any = None) -> Any:
    """Read a field from mapping-like or object-like API responses."""
    if isinstance(result, Mapping):
        return result.get(key, default)
    return getattr(result, key, default)


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
