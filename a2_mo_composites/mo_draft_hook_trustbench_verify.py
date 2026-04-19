# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:204
# Component id: mo.source.ass_ade.hook_trustbench_verify
from __future__ import annotations

__version__ = "0.1.0"

def hook_trustbench_verify(self, action: dict[str, Any]) -> bool | None:
    try:
        from ass_ade.agent.trust_gate import TrustVerificationGate
        gate = TrustVerificationGate(getattr(self, "_v18_config", {}) or {}, self._client)
        ok = gate.pre_action_verify(action)
        self._gate_log.append(GateResult(
            gate="trustbench_verify",
            passed=ok,
            confidence=1.0 if ok else 0.0,
            details={"action": str(action)[:200]},
        ))
        return ok
    except Exception as exc:
        logging.getLogger(__name__).warning("hook_trustbench_verify failed: %s", exc)
        return None
