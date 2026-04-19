# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:581
# Component id: mo.source.ass_ade.reputation_dispute
__version__ = "0.1.0"

    def reputation_dispute(self, entry_id: str, reason: str, **kwargs: Any) -> dict:
        """/v1/reputation/dispute — challenge an entry. $0.080/call"""
        return self._post_raw("/v1/reputation/dispute", {"entry_id": entry_id, "reason": reason, **kwargs})
