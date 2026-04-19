# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:467
# Component id: mo.source.ass_ade.pqcsignresult
__version__ = "0.1.0"

class PqcSignResult(NexusModel):
    """/v1/security/pqc-sign"""
    signature: str | None = None
    algorithm: str | None = None   # "ML-DSA (Dilithium)"
    public_key: str | None = None
