# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_auditreport.py:7
# Component id: mo.source.a2_mo_composites.auditreport
from __future__ import annotations

__version__ = "0.1.0"

class AuditReport:
    total: int
    passed: int
    failed: int
    score: float
    conviction: float
    per_group: dict[str, dict] = field(default_factory=dict)
    failures: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    principles: list[str] = field(default_factory=list)
