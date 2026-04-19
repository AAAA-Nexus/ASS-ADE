# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_lifrgraph.py:18
# Component id: mo.source.a2_mo_composites.store
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
