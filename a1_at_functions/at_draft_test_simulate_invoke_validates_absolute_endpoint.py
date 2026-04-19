# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_simulate_invoke_validates_absolute_endpoint.py:7
# Component id: at.source.a1_at_functions.test_simulate_invoke_validates_absolute_endpoint
from __future__ import annotations

__version__ = "0.1.0"

def test_simulate_invoke_validates_absolute_endpoint(self) -> None:
    """simulate_invoke should validate absolute endpoints for SSRF."""
    from ass_ade.mcp.utils import simulate_invoke

    tool = MCPTool(
        name="bad-tool",
        endpoint="https://127.0.0.1/admin",
        method="POST",
        paid=False,
    )

    with pytest.raises(ValueError, match="blocked network address|loopback"):
        simulate_invoke("https://api.example.com", tool)
