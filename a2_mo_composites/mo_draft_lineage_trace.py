# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:818
# Component id: mo.source.ass_ade.lineage_trace
__version__ = "0.1.0"

    def lineage_trace(self, record_id: str | None = None, *, lineage_id: str | None = None) -> LineageTrace:
        """/v1/lineage/trace/{id} — retrieve + verify chain integrity (DLV-100). $0.020/call"""
        resolved_record_id = record_id or lineage_id or ""
        return self._get_model(f"/v1/lineage/trace/{_pseg(resolved_record_id, 'record_id')}", LineageTrace)
