# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_wisdomengine.py:153
# Component id: mo.source.a2_mo_composites.hydrate_from_memory
from __future__ import annotations

__version__ = "0.1.0"

def hydrate_from_memory(self, *, top_k: int = 10, working_dir: str | Any = ".") -> int:
    """Pre-load principles from prior sessions' persisted vector memory.

    Called at orchestrator init so wisdom carries across sessions. Returns
    the number of principles loaded.
    """
    try:
        from ass_ade.context_memory import query_vector_memory

        result = query_vector_memory(
            query="wisdom principle",
            namespace="wisdom_principle",
            top_k=top_k,
            working_dir=working_dir,
        )
        matches = getattr(result, "matches", None) or []
        loaded: list[str] = []
        for m in matches:
            text = getattr(m, "text", None) or (m.get("text") if isinstance(m, dict) else None)
            if text and text not in loaded and text not in self._principles:
                loaded.append(text)
        if loaded:
            self._principles = (self._principles + loaded)[:20]  # cap at 20
        return len(loaded)
    except Exception as exc:
        _log.debug("WisdomEngine.hydrate_from_memory failed (fail-open): %s", exc)
        return 0
