# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:219
# Component id: mo.source.ass_ade.test_verirand_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_verirand_happy_path(method_name, response_json):
    """Test VeriRand RNG methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "rng_quantum":
            result = client.rng_quantum(count=3)
        else:  # rng_verify
            result = client.rng_verify(seed_ts="ts_123", numbers="123,456,789", proof="proof_123")
        assert result is not None
