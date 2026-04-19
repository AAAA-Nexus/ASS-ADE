# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:300
# Component id: mo.source.ass_ade.hook_verispec_synthesize
from __future__ import annotations

__version__ = "0.1.0"

def hook_verispec_synthesize(self, task: str) -> dict[str, Any] | None:
    try:
        from ass_ade.agent.proofbridge import ProofBridge
        pb = ProofBridge(getattr(self, "_v18_config", {}) or {}, self._client)
        spec = pb.translate(task)
        return {"name": spec.name, "source": spec.source, "has_sorry": spec.has_sorry}
    except Exception as exc:
        logging.getLogger(__name__).warning("hook_verispec_synthesize failed: %s", exc)
        return None
