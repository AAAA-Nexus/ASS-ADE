# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_agent_swarm_routing_happy_path.py:7
# Component id: at.source.a1_at_functions.test_agent_swarm_routing_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_swarm_routing_happy_path(method_name, response_json):
    """Test agent swarm & routing methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "agent_register":
            result = client.agent_register(
                agent_id=324, name="test_agent", capabilities=["execute"],
                endpoint="http://localhost:8000"
            )
        elif method_name == "agent_topology":
            result = client.agent_topology()
        elif method_name == "agent_semantic_diff":
            result = client.agent_semantic_diff(base="version 1", current="version 2")
        elif method_name == "agent_intent_classify":
            result = client.agent_intent_classify(text="execute the plan")
        elif method_name == "agent_token_budget":
            result = client.agent_token_budget(task="analyze text", models=["claude-opus"])
        elif method_name == "agent_contradiction":
            result = client.agent_contradiction(statement_a="it is raining", statement_b="it is sunny")
        elif method_name == "agent_plan":
            result = client.agent_plan(goal="build a system")
        elif method_name == "agent_capabilities_match":
            result = client.agent_capabilities_match(task="find executor")
        elif method_name == "swarm_relay":
            result = client.swarm_relay(from_id="agent_1", to="agent_2", message={"cmd": "execute"})
        elif method_name == "swarm_inbox":
            result = client.swarm_inbox(agent_id="agent_1")
        assert result is not None
