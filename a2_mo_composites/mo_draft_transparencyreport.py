# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:806
# Component id: mo.source.ass_ade.transparencyreport
from __future__ import annotations

__version__ = "0.1.0"

class TransparencyReport(NexusModel):
    """/v1/compliance/transparency — TRP-100"""
    report_id: str | None = None
    period: str | None = None
    pdf_url: str | None = None
    machine_readable: dict | None = None
