# Extracted from C:/!ass-ade/src/ass_ade/agent/wisdom.py:14
# Component id: mo.source.ass_ade.auditreport
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
