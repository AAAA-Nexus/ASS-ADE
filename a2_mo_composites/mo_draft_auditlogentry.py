# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:489
# Component id: mo.source.ass_ade.auditlogentry
from __future__ import annotations

__version__ = "0.1.0"

class AuditLogEntry(NexusModel):
    """/v1/audit/log"""
    entry_id: str | None = None
    hash: str | None = None
    timestamp: Any = None
