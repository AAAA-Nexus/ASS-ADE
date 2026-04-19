# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_nexus_client_fetches_public_contracts.py:7
# Component id: mo.source.a2_mo_composites.test_nexus_client_fetches_public_contracts
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_client_fetches_public_contracts() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payloads = {
            "/health": {"status": "ok"},
            "/openapi.json": {"info": {"version": "0.5.1"}},
            "/.well-known/agent.json": {"name": "AAAA-Nexus", "skills": []},
            "/.well-known/mcp.json": {"name": "AAAA-Nexus", "tools": []},
        }
        return httpx.Response(200, json=payloads[request.url.path])

    transport = httpx.MockTransport(handler)

    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        assert client.get_health().status == "ok"
        assert client.get_openapi().info.version == "0.5.1"
        assert client.get_agent_card().name == "AAAA-Nexus"
        assert client.get_mcp_manifest().name == "AAAA-Nexus"
