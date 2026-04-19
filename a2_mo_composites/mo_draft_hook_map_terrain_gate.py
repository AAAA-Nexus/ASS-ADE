# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:422
# Component id: mo.source.ass_ade.hook_map_terrain_gate
from __future__ import annotations

__version__ = "0.1.0"

def hook_map_terrain_gate(self, ctx: dict[str, Any]) -> dict[str, Any] | None:
    try:
        for method in ("map_terrain", "nexus_map_terrain"):
            fn = getattr(self._client, method, None)
            if fn is None:
                continue
            try:
                result = fn(ctx)
                verdict = getattr(result, "verdict", None)
                if verdict is None and isinstance(result, dict):
                    verdict = result.get("verdict")
                return {"verdict": verdict or "proceed"}
            except Exception:
                break
        return {"verdict": "proceed", "source": "fallback"}
    except Exception as exc:
        logging.getLogger(__name__).warning("hook_map_terrain_gate failed: %s", exc)
        return None
