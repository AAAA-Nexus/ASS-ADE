# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trim_context.py:7
# Component id: at.source.a1_at_functions.trim_context
from __future__ import annotations

__version__ = "0.1.0"

def trim_context(self, context: str, target_tokens: int) -> str | None:
    """Trim context using Nexus memory_trim for optimal token usage.

    Falls back to None if Nexus is unavailable (caller uses local trim).
    """
    try:
        result = self._client.memory_trim(context=context, target_tokens=target_tokens)
        gate = GateResult(
            gate="memory_trim",
            passed=True,
            confidence=1.0,
            details={"target_tokens": target_tokens},
        )
        self._gate_log.append(gate)
        return result.trimmed_context
    except Exception as _exc:  # noqa: BLE001
        logging.getLogger(__name__).warning(
            "Gate %s failed (fail-open): %s: %s",
            "trim_context",
            type(_exc).__name__,
            _exc,
        )
        return None
