# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/errors.py:44
# Component id: mo.source.ass_ade.nexusratelimited
__version__ = "0.1.0"

class NexusRateLimited(NexusError):
    """Rate limit exceeded (429).  Check ``retry_after``."""
