# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:155
# Component id: mo.source.ass_ade.test_trust_oracles_validation_error
__version__ = "0.1.0"

def test_trust_oracles_validation_error(method_name, args):
    """Test trust oracles handle 400 validation errors."""
    transport = httpx.MockTransport(
        lambda r: httpx.Response(400, json={"error": "Invalid input"})
    )
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        with pytest.raises(Exception):
            if method_name == "entropy_oracle":
                getattr(client, method_name)()
            else:
                getattr(client, method_name)(*args)
