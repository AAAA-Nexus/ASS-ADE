# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_capture_trace.py:7
# Component id: at.source.a1_at_functions.capture_trace
from __future__ import annotations

__version__ = "0.1.0"

def capture_trace(self, phase: str, data: dict) -> str:
    text = f"[{phase}] {data.get('summary', str(data)[:200])}"
    meta = {"phase": phase, "data": data, "kind": "trace"}
    result = store_vector_memory(
        text=text,
        namespace=EXPERIENCE_NS,
        metadata=meta,
        working_dir=self._working_dir,
    )
    self._traces += 1
    return result.id
