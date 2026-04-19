# Extracted from C:/!ass-ade/src/ass_ade/agent/lifr_graph.py:37
# Component id: mo.source.ass_ade.store
from __future__ import annotations

__version__ = "0.1.0"

def store(self, spec: str, code: str, proof: str, metadata: dict | None = None) -> str:
    payload = {
        "spec": spec,
        "code": code,
        "proof": proof,
        "metadata": metadata or {},
    }
    meta = dict(metadata or {})
    meta["tier"] = "lifr"
    meta["payload"] = payload
    result = store_vector_memory(
        text=spec,
        namespace=self._namespace,
        metadata=meta,
        working_dir=self._working_dir,
    )
    self._writes += 1
    return result.id
