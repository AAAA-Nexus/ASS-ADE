# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lineage_trace.py:7
# Component id: at.source.a1_at_functions.lineage_trace
from __future__ import annotations

__version__ = "0.1.0"

def lineage_trace(self, record_id: str | None = None, *, lineage_id: str | None = None) -> LineageTrace:
    """/v1/lineage/trace/{id} — retrieve + verify chain integrity (DLV-100). $0.020/call"""
    resolved_record_id = record_id or lineage_id or ""
    return self._get_model(f"/v1/lineage/trace/{_pseg(resolved_record_id, 'record_id')}", LineageTrace)
