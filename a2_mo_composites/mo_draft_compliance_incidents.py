# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1097
# Component id: mo.source.ass_ade.compliance_incidents
__version__ = "0.1.0"

    def compliance_incidents(self, system_id: str, **kwargs: Any) -> dict:
        """/v1/compliance/incidents — incident registry query (INC-101). $0.020/query"""
        return self._get_raw("/v1/compliance/incidents", system_id=system_id, **kwargs)
