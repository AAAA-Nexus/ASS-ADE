# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:474
# Component id: mo.source.ass_ade.complianceresult
__version__ = "0.1.0"

class ComplianceResult(NexusModel):
    """/v1/compliance/check and /v1/compliance/eu-ai-act"""
    compliant: bool | None = None
    frameworks: list[str] = Field(default_factory=list)
    certificate_id: str | None = None
    gaps: list[str] = Field(default_factory=list)
