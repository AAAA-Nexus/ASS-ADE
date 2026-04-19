# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_shield_tool.py:7
# Component id: at.source.a1_at_functions.shield_tool
from __future__ import annotations

__version__ = "0.1.0"

def shield_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any] | None:
    """Shield a tool call through Nexus security."""
    try:
        result = self._client.security_shield({"tool": tool_name, **arguments})
        gate = GateResult(
            gate="tool_shield",
            passed=not (result.blocked or False),
            confidence=1.0,
            details={"tool": tool_name, "sanitized": result.sanitized},
        )
        self._gate_log.append(gate)
        return {
            "blocked": result.blocked or False,
            "sanitized": result.sanitized,
            "reason": "security policy" if result.blocked else None,
        }
    except Exception as _exc:  # noqa: BLE001
        logging.getLogger(__name__).warning(
            "Gate %s failed (fail-open): %s: %s",
            "shield_tool",
            type(_exc).__name__,
            _exc,
        )
        return None
