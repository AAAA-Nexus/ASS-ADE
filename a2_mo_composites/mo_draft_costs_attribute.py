# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1187
# Component id: mo.source.ass_ade.costs_attribute
__version__ = "0.1.0"

    def costs_attribute(self, run_id: str, **kwargs: Any) -> CostAttribution:
        """/v1/costs/attribute — token spend by agent/task/model (DEV-603). $0.040/call"""
        return self._post_model("/v1/costs/attribute", CostAttribution, {"run_id": run_id, **kwargs})
