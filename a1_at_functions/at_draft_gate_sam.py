# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:441
# Component id: at.source.ass_ade.gate_sam
from __future__ import annotations

__version__ = "0.1.0"

def gate_sam(self, target: str, intent: str = "", impl: str = "") -> dict[str, Any] | None:
    """Run SAM TRS scoring + G23 gate as Stage 0 of the pipeline.

    Returns None on failure (fail-open). Logs result to gate_log.
    Blocks synthesis in hybrid/premium if TRS < 0.5.
    """
    try:
        from ass_ade.agent.sam import SAM

        sam = SAM(self._v18_config, self._client)
        trs = sam.compute_trs(target)
        g23_ok = sam.validate_g23(intent, impl) if (intent and impl) else True
        composite = (trs["trust"] + trs["relevance"] + trs["security"]) / 3.0
        passed = composite >= 0.5 and g23_ok
        self._gate_log.append(GateResult(
            gate="sam",
            passed=passed,
            confidence=composite,
            details={"trs": trs, "g23": g23_ok, "composite": composite},
        ))
        # TRS telemetry to Nexus in hybrid/premium
        try:
            if hasattr(self._client, "reputation_record"):
                if composite < 0.7:
                    self._client.reputation_record(
                        "sam_gate", success=False, quality=composite, latency_ms=0.0
                    )
                elif composite >= 0.9:
                    self._client.reputation_record(
                        "sam_gate", success=True, quality=composite, latency_ms=0.0
                    )
        except Exception:
            pass
        return {"trs": trs, "g23": g23_ok, "composite": composite, "passed": passed}
    except Exception as exc:
        logging.getLogger(__name__).warning("gate_sam failed (fail-open): %s", exc)
        return None
