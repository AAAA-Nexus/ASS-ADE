# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_transparencyreport.py:7
# Component id: mo.source.a2_mo_composites.transparencyreport
from __future__ import annotations

__version__ = "0.1.0"

class TransparencyReport(NexusModel):
    """/v1/compliance/transparency — TRP-100"""
    report_id: str | None = None
    period: str | None = None
    pdf_url: str | None = None
    machine_readable: dict | None = None
