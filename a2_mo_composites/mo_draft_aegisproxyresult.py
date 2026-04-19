# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_aegisproxyresult.py:5
# Component id: mo.source.ass_ade.aegisproxyresult
__version__ = "0.1.0"

class AegisProxyResult(NexusModel):
    """/v1/aegis/mcp-proxy/execute"""
    allowed: bool | None = None
    tool_result: dict | None = None
    entropy_bound: float | None = None
    firewall_verdict: str | None = None
