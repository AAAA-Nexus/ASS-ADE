# Extracted from C:/!ass-ade/src/ass_ade/agent/lifr_graph.py:56
# Component id: at.source.ass_ade.query
from __future__ import annotations

__version__ = "0.1.0"

def query(self, spec_text: str, top_k: int = 5) -> list[Match]:
    self._queries += 1
    result = query_vector_memory(
        query=spec_text,
        namespace=self._namespace,
        top_k=top_k,
        working_dir=self._working_dir,
    )
    matches: list[Match] = []
    for m in result.matches:
        if m.score < self._threshold:
            continue
        payload = (m.metadata or {}).get("payload") or {}
        matches.append(
            Match(
                id=m.id,
                score=m.score,
                spec=payload.get("spec", m.text),
                code=payload.get("code", ""),
                proof=payload.get("proof", ""),
                metadata=m.metadata or {},
            )
        )
    return matches
