# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:56
# Component id: at.source.ass_ade.scan_prompt
from __future__ import annotations

__version__ = "0.1.0"

def scan_prompt(self, text: str) -> dict[str, Any] | None:
    """Scan user input for injection attacks."""
    try:
        result = self._client.prompt_inject_scan(text)
        gate = GateResult(
            gate="prompt_scan",
            passed=not (result.threat_detected or False),
            confidence=result.confidence,
            details={"threat_level": result.threat_level},
        )
        self._gate_log.append(gate)
        return {
            "blocked": result.threat_detected or False,
            "threat_level": result.threat_level,
            "confidence": result.confidence,
        }
    except Exception as _exc:  # noqa: BLE001
        logging.getLogger(__name__).warning(
            "Gate %s failed (fail-open): %s: %s",
            "scan_prompt",
            type(_exc).__name__,
            _exc,
        )
        return None
