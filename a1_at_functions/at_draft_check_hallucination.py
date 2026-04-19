# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:81
# Component id: at.source.ass_ade.check_hallucination
from __future__ import annotations

__version__ = "0.1.0"

def check_hallucination(self, text: str) -> dict[str, Any] | None:
    """Check model output for hallucination using ε-KL divergence scoring."""
    try:
        result = self._client.hallucination_oracle(text)
        gate = GateResult(
            gate="hallucination",
            passed=result.verdict != "unsafe",
            confidence=result.confidence,
            details={"verdict": result.verdict, "policy_epsilon": result.policy_epsilon},
        )
        self._gate_log.append(gate)
        return {
            "verdict": result.verdict,
            "confidence": result.confidence,
            "policy_epsilon": result.policy_epsilon,
        }
    except Exception as _exc:  # noqa: BLE001
        logging.getLogger(__name__).warning(
            "Gate %s failed (fail-open): %s: %s",
            "check_hallucination",
            type(_exc).__name__,
            _exc,
        )
        return None
