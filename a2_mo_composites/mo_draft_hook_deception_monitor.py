# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_qualitygates.py:192
# Component id: mo.source.a2_mo_composites.hook_deception_monitor
from __future__ import annotations

__version__ = "0.1.0"

def hook_deception_monitor(self, history: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not history:
        return {"selective_trust": False, "inconsistencies": 0}
    try:
        per_target: dict[str, list[bool]] = {}
        for entry in history:
            target = str(entry.get("target") or entry.get("agent") or "")
            result = bool(entry.get("result", True))
            per_target.setdefault(target, []).append(result)
        inconsistencies = sum(
            1 for outcomes in per_target.values()
            if len(set(outcomes)) > 1 and len(outcomes) >= 3
        )
        selective = inconsistencies >= 2
        self._gate_log.append(GateResult(
            gate="deception_monitor",
            passed=not selective,
            confidence=1.0 - 0.1 * inconsistencies,
            details={"inconsistencies": inconsistencies},
        ))
        return {"selective_trust": selective, "inconsistencies": inconsistencies}
    except Exception as exc:
        logging.getLogger(__name__).warning("hook_deception_monitor failed: %s", exc)
        return None
