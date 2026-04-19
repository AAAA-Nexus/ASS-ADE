# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:545
# Component id: mo.source.ass_ade.escrow_status
__version__ = "0.1.0"

    def escrow_status(self, escrow_id: str) -> EscrowStatus:
        """/v1/escrow/status/{id} — check escrow state. $0.008/call"""
        return self._get_model(f"/v1/escrow/status/{_pseg(escrow_id, 'escrow_id')}", EscrowStatus)
