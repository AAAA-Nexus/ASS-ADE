# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/wisdom.py:14
# Component id: mo.source.ass_ade.auditreport
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
