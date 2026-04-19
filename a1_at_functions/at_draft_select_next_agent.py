# Extracted from C:/!ass-ade/src/ass_ade/agent/puppeteer.py:40
# Component id: at.source.ass_ade.select_next_agent
from __future__ import annotations

__version__ = "0.1.0"

def select_next_agent(self, state: dict) -> AgentRef:
    self._selections += 1
    visited = set(state.get("visited", []))
    if self._policy_available():
        return AgentRef(name="policy", priority=1.0, reason="rl_policy")
    if not self._fallback_dag:
        return AgentRef(name="noop", priority=0.0, reason="no_policy_no_dag")
    for name, prio in self._dag:
        if name not in visited:
            return AgentRef(name=name, priority=prio, reason="dag_fallback")
    return AgentRef(name="done", priority=0.0, reason="dag_exhausted")
