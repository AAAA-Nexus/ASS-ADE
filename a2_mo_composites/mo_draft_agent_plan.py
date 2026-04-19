# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:654
# Component id: mo.source.ass_ade.agent_plan
__version__ = "0.1.0"

    def agent_plan(self, goal: str, **kwargs: Any) -> AgentPlan:
        """/v1/agents/plan — decompose goal into dependency-aware steps. $0.060/request"""
        return self._post_model("/v1/agents/plan", AgentPlan, {"goal": goal, **kwargs})
