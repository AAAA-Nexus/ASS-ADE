# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testx402paymenthandling.py:74
# Component id: at.source.ass_ade.test_post_with_x402_passes_through_on_200
__version__ = "0.1.0"

    def test_post_with_x402_passes_through_on_200(self) -> None:
        """_post_with_x402 should return normal response on 200."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"trust_score": 0.95})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
        assert result == {"trust_score": 0.95}
        client.close()
