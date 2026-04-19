# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_trustverificationgate.py:15
# Component id: at.source.a2_mo_composites.pre_action_verify
from __future__ import annotations

__version__ = "0.1.0"

def pre_action_verify(self, action: dict) -> bool:
    self._checks += 1
    if self._nexus is not None:
        for method in ("trust_gate", "nexus_trust_gate"):
            fn = getattr(self._nexus, method, None)
            if fn is None:
                continue
            try:
                result = fn(action)
                ok = getattr(result, "allowed", None)
                if ok is None and isinstance(result, dict):
                    ok = result.get("allowed")
                if ok is not None:
                    if not ok:
                        self._denied += 1
                    return bool(ok)
            except Exception:
                break
    risk = str(action.get("risk", "")).lower()
    if risk in {"high", "critical"}:
        self._denied += 1
        return False
    return True
