# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_reputation_ledger_happy_path.py:5
# Component id: at.source.ass_ade.test_reputation_ledger_happy_path
__version__ = "0.1.0"

def test_reputation_ledger_happy_path(method_name, response_json):
    """Test reputation ledger methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "reputation_history":
            result = client.reputation_history(agent_id="agent_1")
        else:  # reputation_dispute
            result = client.reputation_dispute(entry_id="entry_123", reason="unfair_score")
        assert result is not None
