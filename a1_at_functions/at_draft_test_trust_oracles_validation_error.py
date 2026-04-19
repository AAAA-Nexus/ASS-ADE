# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trust_oracles_validation_error.py:7
# Component id: at.source.a1_at_functions.test_trust_oracles_validation_error
from __future__ import annotations

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
