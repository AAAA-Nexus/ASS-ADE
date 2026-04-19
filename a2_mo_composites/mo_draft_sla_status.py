# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:598
# Component id: mo.source.ass_ade.sla_status
__version__ = "0.1.0"

    def sla_status(self, sla_id: str) -> SlaStatus:
        """/v1/sla/status/{id} — compliance score + bond remaining. $0.008/call"""
        return self._get_model(f"/v1/sla/status/{_pseg(sla_id, 'sla_id')}", SlaStatus)
